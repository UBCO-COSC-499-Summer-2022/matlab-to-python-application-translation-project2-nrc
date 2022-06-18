from nrcemt.alignment_software.gui.controller_main import MainController
from .window_main import MainWindow
from .controller_main import MainController


def main():
    main_window = MainWindow()
    MainController(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    main()
