import cv2
import numpy as np
import asyncio
import os
import time
from datetime import datetime
from collections import deque
import requests


class UltimateLeaderBrain:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.stream_url = "http://192.168.38.124:81/stream?dummy=.mjpg"

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

        # VideoCapture برای ESP32
        self.cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
        # تلاش برای بهتر کار کردن با استریم ESP32
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not self.cap.isOpened():
            print("WARNING: Cannot open ESP32 stream! چک کنید IP و استریم درست باشه.")

    # =====================
    # Logger Worker (لاگ در فایل)
    # =====================
    async def logger_worker(self):
        log_file = f"brain_{self.robot_id}_log.txt"
        while self.is_running:
            try:
                msg = await self.log_queue.get()
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
                self.log_queue.task_done()
            except Exception as e:
                print("Logger Error:", e)

    # =====================
    # Vision Worker (پردازش تصویر و محاسبه هزینه مسیرها)
    # =====================
    async def vision_worker(self):
        while self.is_running:
            frame = await self.frame_queue.get()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.frame_cache.append(gray)

            if np.mean(gray) < 10:
                await self.cmd_queue.put({"cmd": "stop", "cost": 1.0, "angle": 0, "is_narrow": False})
                await self.log_queue.put("CRITICAL: NO LIGHT - محیط خیلی تاریک")
                continue

            if len(self.frame_cache) < 2:
                continue
            reference_frame = self.frame_cache[0]

            flow = cv2.calcOpticalFlowFarneback(reference_frame, gray, None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            edges = cv2.Canny(gray, 50, 150)

            costs = {}
            for a in self.ANGLES:
                mask, _ = self.get_trapezoid_mask(a)
                m_idx = mask == 255
                if np.sum(m_idx) == 0:
                    costs[a] = 1.0
                    continue

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
    # Command Worker (تصمیم‌گیری و چاپ دستورات در کنسول)
    # =====================
    async def command_worker(self):
        while self.is_running:
            data = await self.cmd_queue.get()
            angle, cost = data['angle'], data['cost']

            # تصمیم‌گیری حرکت
            if cost > self.WALL_LIMIT:
                if time.time() - self.last_180_maneuver > 7:
                    cmd = "turn_right_180"
                    val = 1.0
                    self.last_180_maneuver = time.time()
                    await self.log_queue.put("WALL DETECTED: اجرای مانور 180 درجه")
                else:
                    cmd = "backward"
                    val = 0.4
            elif data.get("is_stuck"):
                cmd = "turn_left_escape"
                val = 0.75
                await self.log_queue.put("STUCK: تلاش برای فرار")
            elif data.get("is_narrow"):
                cmd = "slow_forward"
                val = 0.3
                await self.log_queue.put("NARROW PATH: حرکت آهسته")
            elif angle < 0:
                cmd = "turn_left"
                val = round(1.0 - cost, 2)
            elif angle > 0:
                cmd = "turn_right"
                val = round(1.0 - cost, 2)
            else:
                cmd = "forward"
                val = round(1.0 - cost, 2)

            # چاپ دستور در کنسول (اینجا می‌تونید به ربات بفرستید)
            print(f"🤖 [{self.robot_id}] CMD: {cmd.upper():<18} | VALUE: {val} | ANGLE: {angle:>+4}° | COST: {cost:.2f}")

            await self.log_queue.put(f"CMD: {cmd} | VAL: {val} | A:{angle} | C:{cost}")

    # =====================
    # Receiver Task (خواندن فریم‌ها از استریم)
    # =====================
    
    async def receiver_task(self):
        print("تلاش برای اتصال به استریم...")
        try:
            with requests.get(self.stream_url, stream=True, timeout=20) as r:
                r.raise_for_status()
                bytes_data = b''
                for chunk in r.iter_content(chunk_size=1024):
                    if not self.is_running:
                        break
                    bytes_data += chunk
                    a = bytes_data.find(b'\xff\xd8')
                    b = bytes_data.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes_data[a:b+2]
                        bytes_data = bytes_data[b+2:]
                        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if frame is not None:
                            frame_resized = cv2.resize(frame, (self.W, self.H))
                            if self.frame_queue.full():
                                try:
                                    self.frame_queue.get_nowait()
                                except:
                                    pass
                            await self.frame_queue.put(frame_resized)
        except Exception as e:
            print(f"خطا: {e} — احتمالاً مرورگر بازه یا کلاینت دیگه‌ای وصله")
    # =====================
    # ماسک مسیر (تراپزوئید)
    # =====================
    def get_trapezoid_mask(self, angle):
        mask = np.zeros((self.H, self.W), dtype=np.uint8)
        offset = int((angle / 30.0) * self.W * 0.28)
        pts = np.array([
            [self.W//2 - 20 + offset, 90],
            [self.W//2 + 20 + offset, 90],
            [self.W//2 + 70 + offset, 240],
            [self.W//2 - 70 + offset, 240]
        ], dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)
        return mask, pts

    # =====================
    # اجرا
    # =====================
    async def run(self):
        print(f"--- Brain [{self.robot_id}] Active (بدون MQTT) ---")
        print("دستورات حرکت در کنسول نمایش داده می‌شوند.")
        await asyncio.gather(
            self.receiver_task(),
            self.vision_worker(),
            self.command_worker(),
            self.logger_worker()
        )

    def stop(self):
        self.is_running = False
        self.cap.release()
        print("Brain stopped.")


if __name__ == "__main__":
    brain = UltimateLeaderBrain("LEADER-01")
    try:
        asyncio.run(brain.run())
    except KeyboardInterrupt:
        brain.stop()
