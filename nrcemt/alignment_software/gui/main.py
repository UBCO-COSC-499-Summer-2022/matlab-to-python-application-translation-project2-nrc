import tkinter as tk
from .main_window import MainWindow


def main():
    root = tk.Tk()
    root.geometry("400x300")
    main_window = MainWindow(root)
    main_window.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
