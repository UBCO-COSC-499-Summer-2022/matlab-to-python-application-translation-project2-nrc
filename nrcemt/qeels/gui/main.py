import tkinter as tk
from Main_Window import MainWindow


def main():
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
