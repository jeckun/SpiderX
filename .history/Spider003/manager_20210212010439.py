# -*- coding: utf-8 -*-
import sys
from db import BaseTable


def main(args):
    print('Star Spider...')
    db = BaseTable()
    db.connect()
    row = BaseTable(code='001', name='jeck')
    db.add(row)
    row = BaseTable(code='002', name='frank')
    db.add(row)

    rst = db.session.query()

    for row in db.get_all():
        print(row.id, row.code, row.name, row.createtime, row.modifytime)


if __name__ == "__main__":
    main(sys.argv[1:])
