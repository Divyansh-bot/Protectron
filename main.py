import threading
import json
import time
from modules.network_security import handle_network_security
from modules.user_behavior_monitor import monitor_user_behavior
from modules.file_access_monitor import monitor_file_access
from modules.reverse_shell_monitor import monitor_reverse_shell
from modules.data_exfiltration_monitor import monitor_data_exfiltration
from modules.app_permission_monitor import monitor_app_permissions
from modules.system_call_monitor import monitor_system_calls
from modules.file_integrity_monitor import monitor_file_integrity
from modules.usb_monitor import monitor_usb_security
from dashboard.app import start_dashboard


def update_status(module_name, status):
    try:
        with open("status.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[module_name] = {
        "status": status,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("status.json", "w") as f:
        json.dump(data, f, indent=4)


def start_protectron():
    print("\n🚀 Protectron AI Security System Running...")

    threads = [
        threading.Thread(target=lambda: (update_status("network_security", "running"), handle_network_security())),
        threading.Thread(target=lambda: (update_status("user_behavior", "running"), monitor_user_behavior())),
        threading.Thread(target=lambda: (update_status("file_access", "running"), monitor_file_access())),
        threading.Thread(target=lambda: (update_status("reverse_shell", "running"), monitor_reverse_shell())),
        threading.Thread(target=lambda: (update_status("data_exfiltration", "running"), monitor_data_exfiltration())),
        threading.Thread(target=lambda: (update_status("app_permission", "running"), monitor_app_permissions())),
        threading.Thread(target=lambda: (update_status("system_call", "running"), monitor_system_calls())),
        threading.Thread(target=lambda: (update_status("file_integrity", "running"), monitor_file_integrity())),
        threading.Thread(target=lambda: (update_status("usb_security", "running"), monitor_usb_security())),
        threading.Thread(target=start_dashboard)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_protectron()
