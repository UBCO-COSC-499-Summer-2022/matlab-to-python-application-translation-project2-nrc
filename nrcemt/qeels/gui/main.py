from .main_window import MainWindow


def main():
    root = MainWindow()
    # set title
    root.title("qEEls peak detection")
    # setting size of window
    root.geometry("1500x700")
    # Keeps window visible
    root.mainloop()


if __name__ == "__main__":
    main()
