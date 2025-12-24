import json
import time
import paho.mqtt.client as mqtt

# اگر ساختار پروژه‌ات اینه: Brain/networking/mqtt/...
from networking.mqtt.topics import topics
from networking.mqtt.message_schema import (
    COMMAND_SCHEMA, ERROR_SCHEMA, STATE_SCHEMA, GROUP_SCHEMA,
    WARNING_SCHEMA, STREAM_STATE_SCHEMA
)

# ————————————————————————————————————————
# کمک‌تابع‌ها: اعتبارسنجی خیلی ساده و چاپ مرتب
# ————————————————————————————————————————


def is_json_payload(msg):
    try:
        json.loads(msg)
        return True
    except Exception:
        return False


def pretty_print(label, obj):
    print(f"[{label}] => {json.dumps(obj, ensure_ascii=False, indent=2)}")

# اعتبارسنجی مینیمال مطابق schemaها (ساده، غیرسخت‌گیرانه)


def validate_command(payload: dict) -> bool:
    required = ["robotId", "cmd", "value", "timeStamp"]
    return all(k in payload for k in required)


def validate_state(payload: dict) -> bool:
    required = ["robotId", "battery", "speed", "mode",
                "currentLocation", "status", "timeStamp"]
    return all(k in payload for k in required)


def validate_error(payload: dict) -> bool:
    required = ["robotId", "error-code",
                "severity", "notification", "timeStamp"]
    return all(k in payload for k in required)


def validate_warning(payload: dict) -> bool:
    required = ["robotId", "warning-code",
                "severity", "notification", "timeStamp"]
    return all(k in payload for k in required)


def validate_group(payload: dict) -> bool:
    required = ["robotLeaderId", "cmds", "timeStamp"]
    return all(k in payload for k in required)


def validate_stream_state(payload: dict) -> bool:
    required = ["robotId", "resolution", "internetStatus", "timeStamp", "port"]
    return all(k in payload for k in required)

# ————————————————————————————————————————
# ساخت نمونه پیام‌ها برای تست
# ————————————————————————————————————————


def build_command(robot_id="r1", cmd="forward", value=0.7):
    return {
        "robotId": robot_id,
        "cmd": cmd,
        "value": value,
        "timeStamp": "2025-12-24T18:15:00Z"
    }


def build_state(robot_id="r1"):
    return {
        "robotId": robot_id,
        "battery": 92,
        "speed": 0.5,
        "mode": "ai",
        "currentLocation": "lab",
        "status": "good",
        "timeStamp": "2025-12-24T18:16:00Z"
    }


def build_error(robot_id="r1"):
    return {
        "robotId": robot_id,
        "error-code": "404",
        "severity": "low",
        "notification": {"success": False, "message": "Not found"},
        "timeStamp": "2025-12-24T18:17:00Z"
    }


def build_warning(robot_id="r1"):
    return {
        "robotId": robot_id,
        "warning-code": "300",
        "severity": "medium",
        "notification": {"success": True, "message": "Low battery"},
        "timeStamp": "2025-12-24T18:18:00Z"
    }


def build_group(robot_leader_id="leader-1"):
    return {
        "robotLeaderId": robot_leader_id,
        "cmds": [build_command("r2", "forward", 0.4), build_command("r3", "rotate", 0.2)],
        "timeStamp": "2025-12-24T18:19:00Z"
    }


def build_stream_state(robot_id="r1"):
    return {
        "robotId": robot_id,
        "resolution": 720,
        "internetStatus": "good",
        "timeStamp": "2025-12-24T18:20:00Z",
        "port": 8554
    }

# ————————————————————————————————————————
# مدیریت اتصال و پیام‌ها
# ————————————————————————————————————————


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

    # subscribe روی همهٔ تاپیک‌های اصلی
    # فرض: topics یک دیکشنری با کلیدهای منطقی و مقدار الگوی رشته‌ای است
    # مثلا: topics["command"] = "/robot/{id}/command"
    subs = [
        topics["command"].format(id="r1"),
        topics["state"].format(id="r1"),
        topics["error"].format(id="r1"),
        topics["warning"].format(id="r1"),
        topics["group"],                 # اگر آیدی ندارد و global است
        topics["stream_state"].format(id="r1")
    ]
    for t in subs:
        client.subscribe(t)
        print(f"Subscribed to: {t}")


def on_message(client, userdata, msg):
    raw = msg.payload.decode()
    print(f"Message received: {msg.topic}")
    if not is_json_payload(raw):
        print("Payload is not valid JSON. Raw:", raw)
        return

    payload = json.loads(raw)

    # با توجه به تاپیک، اعتبارسنجی و ثبت
    try:
        if msg.topic == topics["command"].format(id=payload.get("robotId", "r1")):
            ok = validate_command(payload)
            pretty_print("COMMAND", payload)
            if not ok:
                print("Invalid COMMAND payload")

        elif msg.topic == topics["state"].format(id=payload.get("robotId", "r1")):
            ok = validate_state(payload)
            pretty_print("STATE", payload)
            if not ok:
                print("Invalid STATE payload")

        elif msg.topic == topics["error"].format(id=payload.get("robotId", "r1")):
            ok = validate_error(payload)
            pretty_print("ERROR", payload)
            if not ok:
                print("Invalid ERROR payload")

        elif msg.topic == topics["warning"].format(id=payload.get("robotId", "r1")):
            ok = validate_warning(payload)
            pretty_print("WARNING", payload)
            if not ok:
                print("Invalid WARNING payload")

        elif msg.topic == topics["group"]:
            ok = validate_group(payload)
            pretty_print("GROUP", payload)
            if not ok:
                print("Invalid GROUP payload")

        elif msg.topic == topics["stream_state"].format(id=payload.get("robotId", "r1")):
            ok = validate_stream_state(payload)
            pretty_print("STREAM_STATE", payload)
            if not ok:
                print("Invalid STREAM_STATE payload")

        else:
            # wildcard یا تاپیک‌های جدید
            pretty_print("UNKNOWN_TOPIC", {
                         "topic": msg.topic, "payload": payload})

    except Exception as e:
        print("Error processing message:", e)

# ————————————————————————————————————————
# ابزارهای ارسال تست (publish)
# ————————————————————————————————————————


def publish_all_samples(client, robot_id="r1"):
    samples = [
        (topics["command"].format(id=robot_id), build_command(robot_id)),
        (topics["state"].format(id=robot_id), build_state(robot_id)),
        (topics["error"].format(id=robot_id), build_error(robot_id)),
        (topics["warning"].format(id=robot_id), build_warning(robot_id)),
        (topics["group"], build_group("leader-1")),
        (topics["stream_state"].format(id=robot_id),
         build_stream_state(robot_id)),
    ]
    for topic, payload in samples:
        client.publish(topic, json.dumps(payload))
        print(f"Published to {topic}")
        time.sleep(0.3)

# ————————————————————————————————————————
# اجرای کلاینت
# ————————————————————————————————————————


def main():
    # نسخهٔ جدید callback API برای حذف DeprecationWarning
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_start()  # دریافت پیام‌ها در background

    # چند پیام تستی بفرستیم تا همهٔ تاپیک‌ها را ببینیم
    publish_all_samples(client, robot_id="r1")

    # برنامه روشن می‌ماند تا پیام‌ها را دریافت کند
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
