import subprocess
import os
import shutil
import sys
import time

PROJECT_NAME = "Protectron"
VENV_NAME = "protectron_env"
ICON_NAME = "icon.ico"
REQUIREMENTS_FILE = "requirements.txt"

def run(cmd):
    print(f"[~] Running: {cmd}")
    subprocess.call(cmd, shell=True)

def create_virtualenv():
    if not os.path.exists(VENV_NAME):
        print("[+] Creating virtual environment...")
        run(f"python -m venv {VENV_NAME}")
    else:
        print("[=] Virtualenv already exists.")

def install_requirements():
    print("[+] Installing dependencies...")
    pip_path = os.path.join(VENV_NAME, "Scripts", "pip.exe")
    run(f"{pip_path} install -r {REQUIREMENTS_FILE}")

def copy_project():
    install_dir = os.path.expanduser(f"~\\{PROJECT_NAME}")
    if not os.path.exists(install_dir):
        print(f"[+] Copying project to {install_dir}")
        shutil.copytree(os.getcwd(), install_dir, dirs_exist_ok=True)
    return install_dir

def create_startup_shortcut(install_dir):
    import winreg
    exe_path = os.path.join(install_dir, "dist", "Protectron.exe")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Protectron", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print("[+] Auto-start registry key added.")
    except Exception as e:
        print("[-] Failed to add startup key:", e)

def main():
    print("[*] Installing Protectron...")
    create_virtualenv()
    install_requirements()
    target_dir = copy_project()
    create_startup_shortcut(target_dir)
    print("[✔] Installation complete!")
    time.sleep(2)
    print("[+] Launching Protectron...")
    run(f'start {os.path.join(target_dir, "dist", "Protectron.exe")}')

if __name__ == "__main__":
    main()
