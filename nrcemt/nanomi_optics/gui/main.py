import tkinter as tk
from nrcemt.nanomi_optics.engine import nanomi_engine_greeting


def main():
    root = tk.Tk()
    message = tk.Label(root, text=nanomi_engine_greeting())
    message.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
