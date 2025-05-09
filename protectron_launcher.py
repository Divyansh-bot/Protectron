import sys
import ctypes
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from frontend.windows_gui import ProtectronApp


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    app = QApplication(sys.argv)
    window = ProtectronApp()
    window.show()

    # System Tray Icon
    tray_icon = QSystemTrayIcon(QIcon("icon.png"), parent=app)
    tray_icon.setToolTip("Protectron - AI Security")

    tray_menu = QMenu()
    show_action = QAction("Show Protectron")
    quit_action = QAction("Exit")

    show_action.triggered.connect(window.show)
    quit_action.triggered.connect(app.quit)

    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)

    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
