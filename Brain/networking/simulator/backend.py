from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import paho.mqtt.client as mqtt
import json

from networking.mqtt.topics import topics
from networking.hotspot.manager import HotspotManager

app = FastAPI()

# MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# Hotspot Manager
hotspot = HotspotManager()

# -------------------------------
# فرمان‌های اجرایی هر ربات
# -------------------------------


@app.post("/robot/{robot_id}/command")
async def robot_command(robot_id: str, request: Request):
    """
    دریافت فرمان برای یک ربات خاص (forward, backward, left, right, increase_speed, decrease_speed)
    """
    data = await request.json()
    topic = topics["command"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps(data))
    return JSONResponse({"status": "sent", "robot": robot_id, "command": data})

# -------------------------------
# ارسال فرمان گروهی
# -------------------------------


@app.post("/group/command")
async def group_command(request: Request):
    """
    ارسال یک فرمان گروهی به همه ربات‌ها
    """
    data = await request.json()
    topic = topics["group"]
    mqtt_client.publish(topic, json.dumps(data))
    return JSONResponse({"status": "group_sent", "command": data})

# -------------------------------
# Hotspot APIs (برای شبیه‌سازی)
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


@app.get('/')
async def home():
    return JSONResponse({"message": "hello"})
