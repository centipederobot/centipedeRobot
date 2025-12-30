from networking.hotspot.config import HOTSPOT_CONFIG
from networking.hotspot.utils import log, run_command


class HotspotManager:
    def __init__(self, config=HOTSPOT_CONFIG):
        self.config = config

    def start_hotspot(self):
        log("Starting hotspot...")
        cmd_setup = (
            f"netsh wlan set hostednetwork mode=allow "
            f"ssid={self.config['ssid']} key={self.config['password']}"
        )
        run_command(cmd_setup)

        cmd_start = "netsh wlan start hostednetwork"
        output = run_command(cmd_start)
        if output and "started" in output.lower():
            log("Hotspot started successfully")
        else:
            log("Failed to start hotspot")

    def stop_hotspot(self):
        log("Stopping hotspot...")
        cmd = "netsh wlan stop hostednetwork"
        output = run_command(cmd)
        if output and "stopped" in output.lower():
            log("Hotspot stopped successfully")
        else:
            log("Failed to stop hotspot")

    def status(self):
        log("Checking hotspot status...")
        cmd = "netsh wlan show hostednetwork"
        output = run_command(cmd)
        if output and "Status" in output:
            log(output)
            return output
        else:
            log("Could not retrieve hotspot status")
            return None


# تست سریع
if __name__ == "__main__":
    manager = HotspotManager()
    manager.start_hotspot()
    manager.status()
    manager.stop_hotspot()
