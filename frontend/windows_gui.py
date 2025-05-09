import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import BooleanVar
from threading import Thread
import os
import sys
from protectron_app import start_protectron, stop_protectron

# Store toggle state for each module
MODULES = {
    "Network Security": BooleanVar(value=True),
    "User Behavior": BooleanVar(value=True),
    "File Access": BooleanVar(value=True),
    "Reverse Shell": BooleanVar(value=True),
    "Data Exfiltration": BooleanVar(value=True),
    "App Permission": BooleanVar(value=True),
    "System Call": BooleanVar(value=True),
    "File Integrity": BooleanVar(value=True),
    "USB Security": BooleanVar(value=True),
}

# Global thread holder
protectron_thread = None

# Start function wrapper
def start_system():
    global protectron_thread
    if protectron_thread and protectron_thread.is_alive():
        messagebox.showinfo("Protectron", "Protectron is already running.")
        return

    os.environ["MODULE_CONFIG"] = ",".join(
        key.replace(" ", "_").lower() for key, val in MODULES.items() if val.get()
    )
    protectron_thread = Thread(target=start_protectron)
    protectron_thread.start()
    log_box.insert(tk.END, "[INFO] Protectron started.\n")
    log_box.see(tk.END)

# Stop function wrapper
def stop_system():
    stop_protectron()
    log_box.insert(tk.END, "[INFO] Protectron stopped.\n")
    log_box.see(tk.END)

# GUI setup
root = tk.Tk()
root.title("Protectron Security Dashboard")
root.geometry("850x500")
root.resizable(False, False)

# Sidebar for toggles
sidebar = tk.Frame(root, width=200, bg="#2c3e50")
sidebar.pack(side="left", fill="y")

header = tk.Label(sidebar, text="Protectron Modules", bg="#2c3e50", fg="white", font=("Arial", 12, "bold"))
header.pack(pady=10)

for module, var in MODULES.items():
    cb = tk.Checkbutton(sidebar, text=module, variable=var, onvalue=True, offvalue=False,
                        bg="#2c3e50", fg="white", selectcolor="#34495e", activebackground="#2c3e50",
                        font=("Arial", 10))
    cb.pack(anchor="w", padx=10)

# Main area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)

# Buttons
btn_frame = tk.Frame(main_frame, bg="white")
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="Start Protectron", command=start_system, bg="#27ae60", fg="white", padx=20)
start_btn.pack(side="left", padx=10)

stop_btn = tk.Button(btn_frame, text="Stop Protectron", command=stop_system, bg="#c0392b", fg="white", padx=20)
stop_btn.pack(side="left", padx=10)

# Threat Log Display
log_label = tk.Label(main_frame, text="Live Threat Logs", bg="white", font=("Arial", 11, "bold"))
log_label.pack(pady=(20, 5))

log_box = scrolledtext.ScrolledText(main_frame, height=20, width=80, wrap=tk.WORD, font=("Consolas", 10))
log_box.pack(padx=20)

# Run mainloop
root.mainloop()
