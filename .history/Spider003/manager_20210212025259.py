# -*- coding: utf-8 -*-
import sys
from db import Test, AAA


def main(args):
    print('Star Spider...')
    aa = AAA(filename='foo.db')
    aa.connect()
    r = AAA(code='01', name='asd')
    aa.insert(r)

    db = Test()
    db.connect()
    row = Test(code='001', name='frank', age=32)
    db.insert(row)
    row = Test(code='002', name='jeck', age=23)
    db.insert(row)

    rst = db.find(name='jeck')
    db.delete(rst)

    row = Test(code='003', name='black', age=19)
    db.insert(row)
    row.name = 'new name'
    row.age = 18
    db.update(row)

    for row in db.query_all():
        print(row.id, row.code, row.name, row.age,
              row.createtime, row.modifytime)


if __name__ == "__main__":
    main(sys.argv[1:])
