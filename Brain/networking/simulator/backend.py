from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import paho.mqtt.client as mqtt
import json
from datetime import datetime

from networking.mqtt.topics import topics
from networking.hotspot.manager import HotspotManager
from networking.webrtc.connection import WebRTCConnection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ اضافه کردن CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # یا لیست دقیق مثل ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# Hotspot Manager (demo)
hotspot = HotspotManager()

# -------------------------------
# Simulation data
# -------------------------------
COMMANDS = ["forward", "backward", "left",
            "right", "rotate", "rotate-reverse",
            "increase_speed", "decrease_speed"]

robots_status = {
    "r1": {"last_command": None, "connected": False},
    "r2": {"last_command": None, "connected": False},
    "r3": {"last_command": None, "connected": False},
}
command_logs = []  # command history

# -------------------------------
# Robot command API
# -------------------------------


@app.post("/robot/{robot_id}/command")
async def robot_command(robot_id: str, request: Request):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    data = await request.json()
    # Ensure value is an array of 4 numbers
    if "value" in data and (not isinstance(data["value"], list) or len(data["value"]) != 4):
        return JSONResponse({"error": "value must be an array of 4 numbers"}, status_code=400)

    topic = topics["command"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps(data))

    # Update status and logs
    robots_status[robot_id]["last_command"] = data
    command_logs.append({
        "robot": robot_id,
        "action": "robot_command",
        "payload": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })

    return JSONResponse({"status": "sent", "robot": robot_id, "command": data})

# -------------------------------
# Group command API
# -------------------------------


@app.post("/group/command/{robot_id}")
async def group_command(robot_id: str, request: Request):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    data = await request.json()
    # Validate each command in group has value as array of 4 numbers
    if "cmds" in data:
        for cmd in data["cmds"]:
            if "value" in cmd and (not isinstance(cmd["value"], list) or len(cmd["value"]) != 4):
                return JSONResponse({"error": "each command value must be an array of 4 numbers"}, status_code=400)

    topic = topics["group_command"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps(data))

    command_logs.append({
        "robot": robot_id,
        "action": "group_command",
        "payload": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })

    return JSONResponse({"status": "group_sent", "command": data})

# -------------------------------
# Hotspot APIs (demo per robot)
# -------------------------------


@app.post("/hotspot/{robot_id}/start")
async def start_hotspot(robot_id: str):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    robots_status[robot_id]["connected"] = True
    topic = topics["connection"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps({"status": "started"}))

    command_logs.append({
        "robot": robot_id,
        "action": "hotspot_start",
        "time": datetime.utcnow().isoformat() + "Z"
    })
    return JSONResponse({"status": "started", "robot": robot_id})


@app.post("/hotspot/{robot_id}/stop")
async def stop_hotspot(robot_id: str):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    robots_status[robot_id]["connected"] = False
    topic = topics["connection"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps({"status": "stopped"}))

    command_logs.append({
        "robot": robot_id,
        "action": "hotspot_stop",
        "time": datetime.utcnow().isoformat() + "Z"
    })
    return JSONResponse({"status": "stopped", "robot": robot_id})


@app.get("/hotspot/{robot_id}/status")
async def status_hotspot(robot_id: str):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    return JSONResponse({"robot": robot_id, "connected": robots_status[robot_id]["connected"]})

# -------------------------------
# WebRTC APIs (simulation)
# -------------------------------


@app.post("/webrtc/{robot_id}/offer")
async def webrtc_offer(robot_id: str, request: Request):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    data = await request.json()
    answer = {
        "type": "answer",
        "sdp": f"fake-sdp-for-{robot_id}"
    }
    topic = topics["state"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps({"webrtc_offer": data}))

    command_logs.append({
        "robot": robot_id,
        "action": "webrtc_offer",
        "payload": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })
    return JSONResponse({"robot": robot_id, "answer": answer})


@app.get("/webrtc/{robot_id}/status")
async def webrtc_status(robot_id: str):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

    topic = topics["state"].format(id=robot_id)
    mqtt_client.publish(topic, json.dumps({"webrtc_status": "checked"}))

    command_logs.append({
        "robot": robot_id,
        "action": "webrtc_status_check",
        "time": datetime.utcnow().isoformat() + "Z"
    })
    return JSONResponse({
        "robot": robot_id,
        "webrtc": {
            "connected": True,
            "stream": f"/fake-stream/{robot_id}"
        }
    })

# -------------------------------
# Helper APIs
# -------------------------------


@app.get("/robot/{robot_id}/status")
async def robot_status(robot_id: str):
    if robot_id not in robots_status:
        return JSONResponse({"error": "robot not found"}, status_code=404)

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
