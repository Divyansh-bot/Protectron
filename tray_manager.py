import sys
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading

tray_icon = None
tray_thread = None

# Reference to the main window
main_window = None

def show_window():
    if main_window:
        main_window.deiconify()

def quit_app():
    if tray_icon:
        tray_icon.stop()
    if main_window:
        main_window.quit()
        main_window.destroy()
    sys.exit()

def hide_window():
    if main_window:
        main_window.withdraw()

def setup_tray(window_ref):
    global tray_icon, tray_thread, main_window
    main_window = window_ref

    image = Image.open("icon.ico")  # Make sure this icon exists
    
    menu = (
        item('Open Protectron', lambda: show_window()),
        item('Exit', lambda: quit_app())
    )

    tray_icon = pystray.Icon("Protectron", image, "Protectron Running", menu)

    def run_tray():
        tray_icon.run()

    tray_thread = threading.Thread(target=run_tray)
    tray_thread.daemon = True
    tray_thread.start()
