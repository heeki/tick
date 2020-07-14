import json
import sys


def main():
    print("{}".format(json.dumps(sys.path)))


if __name__ == "__main__":
    main()
