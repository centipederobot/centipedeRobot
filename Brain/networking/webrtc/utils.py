import datetime
import uuid


def iso_timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"


def generate_id(prefix="peer"):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def log(message):
    print(f"[{iso_timestamp()}] {message}")
