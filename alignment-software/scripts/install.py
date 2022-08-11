import subprocess
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def install():
    # use pip to install the nrcemt package at its current location
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-e", dir_path])

if __name__ == "__main__":
    install()
    print("DONE! YOU CAN CLOSE THIS WINDOW NOW!")
    input() # wait for user input
