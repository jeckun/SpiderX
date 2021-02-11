# -*- coding: utf-8 -*-
import sys
from db import BaseTable


def main(args):
    print('Star Spider...')
    db = BaseTable()


if __name__ == "__main__":
    main(sys.argv[1:])
