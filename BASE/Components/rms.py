"""
Restaurant Management System 
App is made to facilitate restaurant management processes.

"""

from BASE.Components.mainwindow import MainWindow

from ctypes import windll

# Fix high DPI scaling (for Windows)
try:
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()