# -*- coding: utf-8 -*-
import sys
from db import BaseTable


def main(args):
    print('Star Spider...')
    db = BaseTable()
    db.connect()
    row = BaseTable(code='001', name='jeck')
    db.add(row)


if __name__ == "__main__":
    main(sys.argv[1:])
