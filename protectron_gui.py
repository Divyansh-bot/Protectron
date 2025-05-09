import tkinter as tk
import threading
import logging
from protectron_app import start_protectron, stop_all_threads

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

class ProtectronGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Protectron AI Security System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f4f4f4")

        self.modules = {
            "User Behavior": tk.BooleanVar(value=True),
            "File Access": tk.BooleanVar(value=True),
            "Data Exfiltration": tk.BooleanVar(value=True),
            "Network Security": tk.BooleanVar(value=True),
            "Reverse Shell": tk.BooleanVar(value=True),
            "File Integrity": tk.BooleanVar(value=True),
            "Permission Abuse": tk.BooleanVar(value=True),
            "System Calls": tk.BooleanVar(value=True),
            "USB Security": tk.BooleanVar(value=True),
            "Malware Protection": tk.BooleanVar(value=True)  # ✅ NEW MODULE
        }

        tk.Label(root, text="Protectron Modules", font=("Helvetica", 16, "bold"), bg="#f4f4f4").pack(pady=10)
        for name, var in self.modules.items():
            tk.Checkbutton(root, text=name, variable=var, bg="#f4f4f4", font=("Helvetica", 12)).pack(anchor='w', padx=30)

        tk.Button(root, text="Start Protectron", command=self.start_system, bg="#4caf50", fg="white",
                  font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(pady=10)

        tk.Button(root, text="Stop Protectron", command=self.stop_system, bg="#f44336", fg="white",
                  font=("Helvetica", 12, "bold"), padx=10, pady=5).pack()

        self.console = tk.Text(root, height=12, bg="black", fg="white", font=("Courier", 10))
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_logging()

    def setup_logging(self):
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)

        handler = TextHandler(self.console)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    def start_system(self):
        threading.Thread(target=start_protectron).start()

    def stop_system(self):
        stop_all_threads()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProtectronGUI(root)
    root.mainloop()
