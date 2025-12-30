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
# Simulation data
# -------------------------------
COMMANDS = ["forward", "backward", "left",
            "right", "increase_speed", "decrease_speed"]
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
        "command": data,
        "time": datetime.utcnow().isoformat() + "Z"
    })

    return JSONResponse({"status": "sent", "robot": robot_id, "command": data})

# -------------------------------
# Group command API
# -------------------------------


@app.post("/group/command")
async def group_command(request: Request):
    data = await request.json()
    # Validate each command in group has value as array of 4 numbers
    if "cmds" in data:
        for cmd in data["cmds"]:
            if "value" in cmd and (not isinstance(cmd["value"], list) or len(cmd["value"]) != 4):
                return JSONResponse({"error": "each command value must be an array of 4 numbers"}, status_code=400)

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
# WebRTC APIs (simulation)
# -------------------------------


@app.post("/webrtc/{robot_id}/offer")
async def webrtc_offer(robot_id: str, request: Request):
    """
    Receive Offer from frontend and return simulated Answer
    """
    data = await request.json()
    answer = {
        "type": "answer",
        "sdp": f"fake-sdp-for-{robot_id}"
    }
    return JSONResponse({"robot": robot_id, "answer": answer})


@app.get("/webrtc/{robot_id}/status")
async def webrtc_status(robot_id: str):
    """
    WebRTC status for each robot
    """
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
