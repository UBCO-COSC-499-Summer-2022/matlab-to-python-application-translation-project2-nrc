import subprocess
import sys

def install():
    # use pip to install the nrcemt package at its current location
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-e", "."])

if __name__ == "__main__":
    install()
    print("DONE! YOU CAN CLOSE THIS WINDOW NOW!")
    input() # wait for user input
