#!/usr/bin/python

import sys
from math import floor


def test_poly(string):
    return True if string[:floor(len(string) / 2)] == \
        string[-floor(len(string) / 2):][::-1] else False


if __name__ == "__main__":
    if len(sys.argv) == 2:
        string = sys.argv[1]
        print(test_poly(string))
    else:
        print("wrong arguments")
