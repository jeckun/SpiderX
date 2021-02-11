# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime

Base = declarative_base()


class BaseTable(Base):
    __tablename__ = ''
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    gmt_create = Column(DateTime, server_default=datetime.now())
    gmt_modify = Column(DateTime, nullable=False,
                        server_default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return ""
