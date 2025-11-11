# main.py
import tkinter as tk
from gui.interface import LocalVaultApp
import sys

def main():
    try:
        root = tk.Tk()
        app = LocalVaultApp(root)
        root.mainloop()
    except Exception as e:
        print(f"[Error crítico] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
