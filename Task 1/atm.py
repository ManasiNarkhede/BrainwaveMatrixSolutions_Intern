import tkinter as tk
from gui import ATMGUI

if __name__ == "__main__":
    root = tk.Tk()
    atm_app = ATMGUI(root)
    root.mainloop()