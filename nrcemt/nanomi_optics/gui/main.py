# Nanomi Optics GUI
from .main_window import MainWindow


def main():
    # application
    # window creation
    root = MainWindow()
    # set title of window
    root.title('Nanomi Optics')
    # set window size
    root.geometry('1200x800')

    # keep the window open
    root.mainloop()


if __name__ == "__main__":
    main()
