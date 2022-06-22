# Nanomi Optics GUI
from .main_window import MainWindow


def main():
    # application
    # window creation
    root = MainWindow()
    # keep the window open
    root.mainloop()


if __name__ == "__main__":
    main()
