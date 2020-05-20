import sys

from .version import EasyhtmltableAbout as About


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    print("Easy HTML Table main()")
    print("%s" % About())
    if argv:
        print("args:")
        for arg in argv:
            print(arg)
    else:
        print("No args provided")


if __name__ == "__main__":
    main(sys.argv[1:])
