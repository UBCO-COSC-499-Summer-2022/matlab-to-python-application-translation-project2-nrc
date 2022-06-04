import tkinter as tk
from nrcemt.alignment_software.engine import alignment_engine_greeting


def main():
    root = tk.Tk()
    message = tk.Label(root, text=alignment_engine_greeting())
    message.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
