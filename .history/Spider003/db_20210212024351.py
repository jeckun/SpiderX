# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import uuid4
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Engine:
    def __init__(self, filename, cache=True):
        self.__filename__ = filename
        self.__cache__ = cache

    def connect(self, echo=False):

        if self.__cache__:
            self.engine = create_engine('sqlite:///:memory:', echo=echo)
        else:
            db_path = 'sqlite:///' + filename
            self.engine = create_engine(db_path, echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def insert(self, row):
        self.session.add(row)
        self.session.commit()

    def delete(self, row):
        if type(row) == sqlalchemy.orm.query.Query:
            [self.session.delete(u) for u in row]
        elif type(row) == type(self):
            self.session.delete(row)
        self.session.commit()

    def update(self, row):
        self.session.commit()

    def find(self, **kwargs):
        cmd = "self.session.query(%s)" % self.__class__.__name__
        for kw in kwargs:
            cmd += ".filter(%s.%s == '%s')" % (self.__class__.__name__, kw,
                                               kwargs[kw])
        cmd += ".first()"
        return eval(cmd)

    def filter(self, **kwargs):
        cmd = "self.session.query(%s)" % self.__class__.__name__
        for kw in kwargs:
            cmd += ".filter(%s.%s == '%s')" % (self.__class__.__name__, kw,
                                               kwargs[kw])
        return eval(cmd)

    def query_all(self):
        cmd = "self.session.query(%s).all()" % self.__class__.__name__
        return eval(cmd)


class Test(Base, Engine):
    __tablename__ = 'Test'
    key = Column(String(36), nullable=False,
                 default=str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, default=0)
    createtime = Column(
        DateTime, server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modifytime = Column(DateTime, nullable=False,
                        server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), onupdate=datetime.now())
