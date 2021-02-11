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
    key = Column(String(36), unique=True, nullable=False,
                 default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    createtime = Column(
        DateTime, server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modifytime = Column(DateTime, nullable=False,
                        server_default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def connect(self):
        # engine = create_engine('sqlite:///foo.db')
        self.engine = create_engine('sqlite:///:memory:', echo=True,
                                    check_same_thread=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, row):
        self.session.add(row)
        self.session.commit()

    def get_all(self):
        return self.session.query(BaseTable).all()
