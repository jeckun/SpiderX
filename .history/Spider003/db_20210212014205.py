# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import uuid4
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BaseTable(Base):
    __tablename__ = 'BaseTable'
    key = Column(String(36), nullable=False,
                 default=str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    createtime = Column(
        DateTime, server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modifytime = Column(DateTime, nullable=False,
                        server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), onupdate=datetime.now())

    def connect(self):
        # engine = create_engine('sqlite:///foo.db')
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def add(self, row):
        self.session.add(row)
        self.session.commit()

    def delete(self, row):
        self.session.delete(row)
        self.session.commit()

    def update(self, row):
        self.session.commit()

    def query(self, **kwargs):
        cmd = "self.session.query(BaseTable)"
        for kw in kwargs:
            cmd += ".filter(BaseTable.%s == '%s')" % (kw, kwargs[kw])
        cmd += ".first()"
        return eval(cmd)

    def get_all(self):
        return self.session.query(BaseTable).all()


class Test(BaseTable):
    __tablename__ = 'test'
    age = 0
