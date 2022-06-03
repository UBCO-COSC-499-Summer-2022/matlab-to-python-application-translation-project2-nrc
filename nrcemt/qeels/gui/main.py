import tkinter as tk
from nrcemt.qeels.engine import qeels_engine_greeting


def main():
    root = tk.Tk()
    message = tk.Label(root, text=qeels_engine_greeting())
    message.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
