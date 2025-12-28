from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import paho.mqtt.client as mqtt
import json
from datetime import datetime

from networking.mqtt.topics import topics
from networking.hotspot.manager import HotspotManager
from networking.webrtc.connection import WebRTCConnection

app = FastAPI()

# MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# Hotspot Manager
hotspot = HotspotManager()

# -------------------------------
# داده‌های شبیه‌سازی
# -------------------------------
COMMANDS = ["forward", "backward", "left",
            "right", "increase_speed", "decrease_speed"]
robots_status = {
    "r1": {"last_command": None, "connected": True},
    "r2": {"last_command": None, "connected": True},
    "r3": {"last_command": None, "connected": True},
}
command_logs = []  # تاریخچه فرمان‌ها

# -------------------------------
# فرمان‌های اجرایی هر ربات
# -------------------------------


@app.post("/robot/{robot_id}/command")
async def robot_command(robot_id: str, request: Request):
    data = await request.json()
    topic = topics["command"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps(data))

    # ثبت وضعیت و لاگ
    robots_status[robot_id]["last_command"] = data
    command_logs.append({
        "robot": robot_id,
        "command": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })

    return JSONResponse({"status": "sent", "robot": robot_id, "command": data})

# -------------------------------
# ارسال فرمان گروهی
# -------------------------------


@app.post("/group/command")
async def group_command(request: Request):
    data = await request.json()
    topic = topics["group"]
    mqtt_client.publish(topic, json.dumps(data))

    command_logs.append({
        "robot": "group",
        "command": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })

    return JSONResponse({"status": "group_sent", "command": data})

# -------------------------------
# Hotspot APIs
# -------------------------------


@app.post("/hotspot/start")
async def start_hotspot():
    hotspot.start_hotspot()
    return JSONResponse({"status": "started"})


@app.post("/hotspot/stop")
async def stop_hotspot():
    hotspot.stop_hotspot()
    return JSONResponse({"status": "stopped"})


@app.get("/hotspot/status")
async def status_hotspot():
    status = hotspot.status()
    return JSONResponse({"status": status})

# -------------------------------
# WebRTC APIs (شبیه‌سازی)
# -------------------------------


@app.post("/webrtc/{robot_id}/offer")
async def webrtc_offer(robot_id: str, request: Request):
    """
    دریافت Offer از فرانت و برگرداندن Answer شبیه‌سازی‌شده
    """
    data = await request.json()
    # در حالت واقعی باید PeerConnection ساخته شود
    # اینجا فقط شبیه‌سازی می‌کنیم
    answer = {
        "type": "answer",
        "sdp": f"fake-sdp-for-{robot_id}"
    }
    return JSONResponse({"robot": robot_id, "answer": answer})


@app.get("/webrtc/{robot_id}/status")
async def webrtc_status(robot_id: str):
    """
    وضعیت WebRTC برای هر ربات
    """
    return JSONResponse({
        "robot": robot_id,
        "webrtc": {
            "connected": True,
            "stream": f"/fake-stream/{robot_id}"
        }
    })

# -------------------------------
# APIهای کمکی
# -------------------------------


@app.get("/robot/{robot_id}/status")
async def robot_status(robot_id: str):
    return JSONResponse({"robot": robot_id, "status": robots_status.get(robot_id)})


@app.get("/commands/list")
async def list_commands():
    return JSONResponse({"commands": COMMANDS})


@app.get("/commands/logs")
async def get_logs():
    return JSONResponse({"logs": command_logs})


@app.get('/')
async def home():
    return JSONResponse({"message": "hello"})
