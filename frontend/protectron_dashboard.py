import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os

# Mapping of model names to module import paths and function calls
MODEL_CONFIG = {
    "Network Intrusion": ("modules.network_intrusion_realtime", "start_intrusion_monitor"),
    "User Behavior": ("modules.user_behavior_monitor", "monitor_user_behavior"),
    "File Access": ("modules.file_access_management", "monitor_file_access"),
    "Reverse Shell": ("modules.reverse_shell_monitor", "monitor_reverse_shell"),
    "Data Exfiltration": ("modules.data_exfiltration_monitor", "monitor_data_exfiltration"),
    "App Permission": ("modules.permission_monitor", "monitor_app_permissions"),
    "System Call": ("modules.systemcall_monitor", "monitor_system_calls"),
    "File Integrity": ("modules.file_integrity_monitor", "monitor_file_integrity"),
    "USB Security": ("modules.usb_monitor", "monitor_usb_security"),
}

module_threads = {}
module_status = {name: False for name in MODEL_CONFIG.keys()}

# Logger for live updates
def log_event(text):
    log_console.config(state='normal')
    log_console.insert(tk.END, text + '\n')
    log_console.see(tk.END)
    log_console.config(state='disabled')

# Start individual module
def start_module(name):
    if not module_status[name]:
        module_status[name] = True
        log_event(f"✅ Starting {name}...")
        module_path, func_name = MODEL_CONFIG[name]
        mod = __import__(module_path, fromlist=[func_name])
        func = getattr(mod, func_name)
        thread = threading.Thread(target=func)
        thread.start()
        module_threads[name] = thread

# Stop is logical toggle only (no internal interrupt unless built-in)
def stop_module(name):
    if module_status[name]:
        module_status[name] = False
        log_event(f"🛑 {name} turned off. Please restart app to fully unload.")

# Toggle callback

def toggle_module(name):
    if module_vars[name].get():
        start_module(name)
    else:
        stop_module(name)

# Initialize GUI
root = tk.Tk()
root.title("🛡️ Protectron - AI Security System")
root.geometry("850x650")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")
style.configure("TCheckbutton", background="#1e1e1e", foreground="white")
style.configure("TLabel", background="#1e1e1e", foreground="white")

header = ttk.Label(root, text="PROTECTRON SECURITY MODULES", font=("Segoe UI", 20, "bold"))
header.pack(pady=20)

module_frame = ttk.Frame(root)
module_frame.pack(pady=10)

# Create module checkboxes
module_vars = {}
row = 0
col = 0
for name in MODEL_CONFIG:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(module_frame, text=name, variable=var, command=lambda n=name: toggle_module(n))
    chk.grid(row=row, column=col, padx=15, pady=10, sticky="w")
    module_vars[name] = var
    col += 1
    if col >= 3:
        col = 0
        row += 1

# Logging Console
log_label = ttk.Label(root, text="Live Threat & Action Logs")
log_label.pack(pady=10)

log_console = scrolledtext.ScrolledText(root, height=15, width=100, bg="#2e2e2e", fg="lime", font=("Consolas", 10))
log_console.pack()
log_console.config(state='disabled')

# Run GUI loop
def launch_gui():
    root.mainloop()

if __name__ == "__main__":
    launch_gui()