import tkinter as tk
from nrcemt.qeels.engine import qeels_engine_greeting
from MainWindow import MainWindow


def main():
    print(qeels_engine_greeting())
    root = tk.Tk()
    # set title
    root.title("qEEls peak detection")
    # setting size of window(will change later)
    root.geometry("1500x700")
    # creates actuall window with all widgets
    main_window = MainWindow(root)
    main_window.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
