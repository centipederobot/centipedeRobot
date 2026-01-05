import cv2
import numpy as np
import asyncio
import os
import json
import time
from datetime import datetime
from collections import deque
import paho.mqtt.client as mqtt

# =======================
# تاپیک‌های MQTT
# =======================
try:
    from topics import topics
except ImportError:
    topics = {
        "command": "/robot/{id}/command",
        "group_command": "/robot/group/all/group_command",
        "warning": "/robot/{id}/warning"
    }

class UltimateLeaderBrain:
    def __init__(self, robot_id, esp32_ip, mqtt_broker):
        self.robot_id = robot_id
        self.stream_url = f"http://{esp32_ip}/mjpeg/stream"  # بهینه شده
        self.mqtt_broker = mqtt_broker

        # پارامترهای پردازش تصویر
        self.W, self.H = 320, 240
        self.ANGLES = [-30, -20, -10, 0, 10, 20, 30]
        self.FLOW_TH = 1.1
        self.EDGE_TH = 0.08
        self.SHADOW_TH = 35
        self.WALL_LIMIT = 0.92

        # حافظه و کش
        self.frame_cache = deque(maxlen=30)
        self.path_memory = {a: deque(maxlen=15) for a in self.ANGLES}

        # صف‌های asyncio
        self.frame_queue = asyncio.Queue(maxsize=1)
        self.cmd_queue = asyncio.Queue()
        self.log_queue = asyncio.Queue()

        self.is_running = True
        self.last_180_maneuver = 0
        self.client = mqtt.Client()

        # VideoCapture برای ESP32
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap.isOpened():
            print("WARNING: Cannot open ESP32 stream!")

    # =====================
    # Logger Worker
    # =====================
    async def logger_worker(self):
        max_bytes = 2048
        log_files = [f"brain_{self.robot_id}_A.log", f"brain_{self.robot_id}_B.log"]
        current_idx = 0
        while self.is_running:
            try:
                msg = await self.log_queue.get()
                log_path = log_files[current_idx]
                if os.path.exists(log_path) and os.path.getsize(log_path) >= max_bytes:
                    current_idx = 1 - current_idx
                    log_path = log_files[current_idx]
                    if os.path.exists(log_path): os.remove(log_path)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().strftime('%M:%S')}] {msg}\n")
                self.log_queue.task_done()
            except Exception as e:
                print("Logger Error:", e)

    # =====================
    # Vision Worker
    # =====================
    async def vision_worker(self):
        while self.is_running:
            frame = await self.frame_queue.get()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.frame_cache.append(gray)

            if np.mean(gray) < 10:
                await self.cmd_queue.put({"cmd": "stop", "cost": 1.0, "angle": 0, "is_narrow": False})
                await self.log_queue.put("CRITICAL: NO LIGHT")
                continue

            if len(self.frame_cache) < 2: continue
            reference_frame = self.frame_cache[0]

            flow = cv2.calcOpticalFlowFarneback(reference_frame, gray, None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            edges = cv2.Canny(gray, 50, 150)

            costs = {}
            for a in self.ANGLES:
                mask, _ = self.get_trapezoid_mask(a)
                m_idx = mask == 255
                f_mean = np.mean(mag[m_idx])
                e_density = np.sum(edges[m_idx] > 0) / np.sum(m_idx)
                brightness_diff = np.mean(reference_frame[m_idx]) - np.mean(gray[m_idx])

                is_shadow = brightness_diff > self.SHADOW_TH and e_density < 0.04
                is_passable = f_mean < 0.7 and e_density < 0.07

                cost = 0.15 if (is_shadow or is_passable) else min(1.0, (f_mean * 0.4) + (e_density * 3.5))
                costs[a] = round(cost, 3)

            best_a = min(costs, key=costs.get)
            is_stuck = np.mean(mag) < 0.08 and len(self.frame_cache) > 25

            await self.cmd_queue.put({
                "angle": best_a,
                "cost": costs[best_a],
                "costs": costs,
                "frame": frame,
                "is_stuck": is_stuck,
                "is_narrow": costs[self.ANGLES[0]] > 0.65 and costs[self.ANGLES[-1]] > 0.65
            })

    # =====================
    # Publisher Worker
    # =====================
    async def publisher_worker(self):
        self.client.connect(self.mqtt_broker, 1883)
        self.client.loop_start()
        while self.is_running:
            data = await self.cmd_queue.get()
            angle, cost = data['angle'], data['cost']

            # تصمیم‌گیری
            if cost > self.WALL_LIMIT:
                if time.time() - self.last_180_maneuver > 7:
                    cmd, val = "turn_right", [1.0]
                    self.last_180_maneuver = time.time()
                    await self.log_queue.put("WALL: EXECUTING 180 TURN")
                else:
                    cmd, val = "backward", [0.4]
            elif data.get("is_stuck"):
                cmd, val = "turn_left", [0.75]
                await self.log_queue.put("STUCK: ATTEMPTING ESCAPE")
            elif angle < 0: cmd, val = "turn_left", [round(1.0 - cost, 2)]
            elif angle > 0: cmd, val = "turn_right", [round(1.0 - cost, 2)]
            else: cmd, val = "forward", [round(1.0 - cost, 2)]

            payload = {
                "robotId": self.robot_id,
                "cmd": cmd,
                "value": val,
                "angle": abs(angle),
                "is_narrow": data.get("is_narrow", False),
                "timeStamp": datetime.now().isoformat()
            }

            self.client.publish(topics["command"].format(id=self.robot_id), json.dumps(payload))
            self.manage_swarm_sync(payload)
            await self.log_queue.put(f"{cmd} | A:{angle} | C:{cost}")

    # =====================
    # Receiver Task (با VideoCapture)
    # =====================
    async def receiver_task(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue
            frame_resized = cv2.resize(frame, (self.W, self.H))
            if self.frame_queue.full():
                self.frame_queue.get_nowait()
            await self.frame_queue.put(frame_resized)
            await asyncio.sleep(0)  # اجازه می‌دهد حلقه asyncio اجرا شود

    # =====================
    # Swarm Coordination
    # =====================
    def manage_swarm_sync(self, leader_payload):
        group_cmd = leader_payload.copy()
        if leader_payload["is_narrow"]:
            group_cmd["cmd"], group_cmd["value"] = "slow_speed", [0.12]
        swarm_msg = {
            "robotLeaderId": self.robot_id,
            "cmds": [group_cmd],
            "timeStamp": leader_payload["timeStamp"]
        }
        self.client.publish(topics["group_command"].format(id="all"), json.dumps(swarm_msg))

    # =====================
    # ماسک مسیر
    # =====================
    def get_trapezoid_mask(self, angle):
        mask = np.zeros((self.H, self.W), dtype=np.uint8)
        offset = int((angle / 30.0) * self.W * 0.28)
        pts = np.array([
            [self.W//2 - 20 + offset, 90], [self.W//2 + 20 + offset, 90],
            [self.W//2 + 70 + offset, 240], [self.W//2 - 70 + offset, 240]
        ], dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)
        return mask, pts

    # =====================
    # اجرا
    # =====================
    async def run(self):
        print(f"--- Brain [{self.robot_id}] Active ---")
        await asyncio.gather(
            self.receiver_task(),
            self.vision_worker(),
            self.logger_worker(),
            self.publisher_worker()
        )


if __name__ == "__main__":
    brain = UltimateLeaderBrain("LEADER-01", "192.168.1.50", "localhost")
    try:
        asyncio.run(brain.run())
    except KeyboardInterrupt:
        brain.is_running = False
        brain.cap.release()
        print("Brain stopped.")
