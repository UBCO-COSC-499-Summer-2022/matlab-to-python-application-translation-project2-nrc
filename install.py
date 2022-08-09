import subprocess
import sys

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-e", "."])

if __name__ == "__main__":
    install()
    print("DONE! YOU CAN CLOSE THIS WINDOW NOW!")
    input()
