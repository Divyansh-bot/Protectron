import os
import sys
import subprocess
import platform
from utils.database_handler import MongoDBHandler

db_handler = MongoDBHandler()

def is_admin():
    """Check if the script is running as Administrator (Windows) or Root (Linux/macOS)."""
    if platform.system() == "Windows":
        try:
            return os.getuid() == 0
        except AttributeError:
            return "Admin" in subprocess.run("whoami /priv", capture_output=True, text=True).stdout
    return os.geteuid() == 0

def run_as_admin():
    """Automatically relaunch Protectron with Administrator privileges."""
    if not is_admin():
        print("⚠️ Protectron needs to run as Administrator to block threats.")
        if platform.system() == "Windows":
            subprocess.run(["powershell", "Start-Process", "python", "-ArgumentList", f"'{sys.argv[0]}'", "-Verb", "runAs"])
        sys.exit()

def block_ip(ip_address):
    """Blocks a given IP address using the system firewall."""
    system_os = platform.system()
    
    run_as_admin()  # 🔥 Automatically request Admin privileges

    try:
        if system_os == "Windows":
            # ✅ Windows Firewall command to block IP
            command = f'netsh advfirewall firewall add rule name="Protectron Block {ip_address}" dir=in action=block remoteip={ip_address}'
        elif system_os == "Linux":
            # ✅ Linux iptables command
            command = f'sudo iptables -A INPUT -s {ip_address} -j DROP'
        elif system_os == "Darwin":  # macOS
            # ✅ macOS firewall command
            command = f'sudo pfctl -t blocklist -T add {ip_address}'
        else:
            print(f"⚠️ Unsupported OS: {system_os}")
            return

        subprocess.run(command, shell=True, check=True)
        print(f"🔥 BLOCKED: {ip_address}")

        # ✅ Log the blocked IP in MongoDB
        db_handler.insert_log("blocked_ips", {"ip_address": ip_address, "status": "blocked"})

    except Exception as e:
        print(f"❌ Failed to block IP: {e}")

def kill_process(process_name):
    """Terminates a given process."""
    system_os = platform.system()

    try:
        if system_os == "Windows":
            command = f'taskkill /IM {process_name} /F'
        else:
            command = f'pkill -f {process_name}'

        subprocess.run(command, shell=True, check=True)
        print(f"🔴 Killed process: {process_name}")

    except Exception as e:
        print(f"❌ Failed to kill process: {e}")
