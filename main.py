import tkinter as tk
from SysMon.system_monitor import *

if __name__ == "__main__":
    root = tk.Tk()
    monitor = SystemMonitor(root)
    root.mainloop()
