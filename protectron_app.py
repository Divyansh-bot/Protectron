import threading
import logging

from modules.user_behavior_monitor import monitor_user_behavior
from modules.file_access_management import monitor_file_access
from modules.data_exfiltration_monitor import monitor_data_exfiltration
from modules.network_intrusion_monitor import start_intrusion_monitor
from modules.reverse_shell_monitor import monitor_reverse_shell
from modules.permission_monitor import monitor_app_permissions
from modules.systemcall_monitor import monitor_system_calls
from modules.file_integrity_monitor import monitor_file_integrity
from modules.usb_monitor import monitor_usb_security
from hybrid_ai.scanner.hybrid_scanner import start_hybrid_scanner

# Global stop event and thread list
stop_event = threading.Event()
threads = []

def start_protectron():
    logging.info("🚀 Starting Protectron AI Security System...")
    modules = [
        monitor_user_behavior,
        monitor_file_access,
        monitor_data_exfiltration,
        start_intrusion_monitor,
        monitor_reverse_shell,
        monitor_app_permissions,
        monitor_system_calls,
        monitor_file_integrity,
        monitor_usb_security,
        start_hybrid_scanner,  # ✅ Add Hybrid AI module here
    ]
    for module in modules:
        t = threading.Thread(target=module, args=(stop_event,), daemon=True)
        threads.append(t)
        t.start()

def stop_all_threads():
    stop_event.set()
    logging.info("🛑 Stopping all Protectron modules...")
    for t in threads:
        if t.is_alive():
            t.join()
