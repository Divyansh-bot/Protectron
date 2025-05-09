import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import pystray
from PIL import Image, ImageTk

# === Launch backend ===
def start_protectron_backend():
    try:
        subprocess.Popen([sys.executable, "protectron_app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log_output.insert(tk.END, "[+] Protectron backend started.\n")
    except Exception as e:
        log_output.insert(tk.END, f"[!] Failed to start Protectron backend: {e}\n")

# === Stop logic placeholder ===
def stop_protectron_backend():
    messagebox.showinfo("Stop Protectron", "To stop Protectron, close this window or terminate background tasks manually.")

# === GUI Window ===
def create_gui():
    global log_output

    root = tk.Tk()
    root.title("Protectron - AI Security System")
    root.geometry("850x600")
    root.configure(bg="#1f1f1f")

    # Title
    tk.Label(root, text="PROTECTRON", font=("Segoe UI", 24, "bold"), fg="#00ffae", bg="#1f1f1f").pack(pady=10)

    # Module toggles (Visual only)
    flags = {
        "Network Security": tk.BooleanVar(value=True),
        "User Behavior": tk.BooleanVar(value=True),
        "File Access": tk.BooleanVar(value=True),
        "Reverse Shell": tk.BooleanVar(value=True),
        "Data Exfiltration": tk.BooleanVar(value=True),
        "App Permissions": tk.BooleanVar(value=True),
        "System Calls": tk.BooleanVar(value=True),
        "File Integrity": tk.BooleanVar(value=True),
        "USB Monitor": tk.BooleanVar(value=True),
    }

    toggle_frame = tk.Frame(root, bg="#1f1f1f")
    toggle_frame.pack(pady=10)
    for i, (name, var) in enumerate(flags.items()):
        cb = ttk.Checkbutton(toggle_frame, text=name, variable=var)
        cb.grid(row=i // 3, column=i % 3, padx=15, pady=10, sticky="w")

    # Buttons
    button_frame = tk.Frame(root, bg="#1f1f1f")
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="▶ Start Protectron", command=start_protectron_backend).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="■ Stop Protectron", command=stop_protectron_backend).grid(row=0, column=1, padx=10)

    # Output log
    log_output = tk.Text(root, height=15, bg="#101010", fg="#00ffae", font=("Consolas", 10))
    log_output.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    log_output.insert(tk.END, "[+] Welcome to Protectron GUI Interface\n")

    # === System Tray Integration ===
    def minimize_to_tray():
        root.withdraw()
        image = Image.open("icon.ico") if os.path.exists("icon.ico") else None

        def on_restore(icon, item):
            icon.stop()
            root.after(0, root.deiconify)

        def on_quit(icon, item):
            icon.stop()
            root.destroy()

        menu = pystray.Menu(
            pystray.MenuItem("Restore Protectron", on_restore),
            pystray.MenuItem("Exit", on_quit)
        )
        icon = pystray.Icon("Protectron", image, "Protectron", menu)
        icon.run()

    root.protocol("WM_DELETE_WINDOW", minimize_to_tray)
    root.mainloop()

# Run GUI
if __name__ == "__main__":
    create_gui()
