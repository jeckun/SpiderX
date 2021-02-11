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

    # rst = db.session.query(BaseTable).filter(BaseTable.id == 2).first()
    # rst = db.query(name='frank')
    rst = db.query(id=2)
    rst.name = 'new name'
    db.update(rst)

    row = BaseTable(code='003', name='black')
    db.add(row)
    db.delete(rst)

    for row in db.get_all():
        print(row.id, row.code, row.name, row.createtime, row.modifytime)


if __name__ == "__main__":
    main(sys.argv[1:])
