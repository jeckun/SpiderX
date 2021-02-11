# -*- coding: utf-8 -*-
import sys
from db import Test


def main(args):
    print('Star Spider...')
    db = Test()
    db.connect()
    row = Test(code='001', name='jeck', age=32)
    db.add(row)
    row = Test(code='002', name='frank', age=23)
    db.add(row)

    rst = db.query(code='001', name='jeck')
    rst.name = 'new name'
    db.update(rst)

    row = Test(code='003', name='black')
    db.add(row)
    db.delete(rst)

    for row in db.get_all():
        print(row.id, row.code, row.name, row.createtime, row.modifytime)


if __name__ == "__main__":
    main(sys.argv[1:])
