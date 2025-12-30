import datetime
import subprocess


def iso_timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"


def log(message):
    print(f"[{iso_timestamp()}] {message}")


def run_command(cmd):
    """اجرای دستور ویندوز و برگرداندن خروجی"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            log(f"Error running command: {result.stderr}")
            return None
    except Exception as e:
        log(f"Exception: {e}")
        return None
