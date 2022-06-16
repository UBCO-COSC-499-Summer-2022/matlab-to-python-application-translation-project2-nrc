from nrcemt.qeels.engine.prz import load_prz
import os
def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'resources\\1_qEELS_1deg_sum.prz')
    load_prz(filename)


if __name__ == "__main__":
    main()
