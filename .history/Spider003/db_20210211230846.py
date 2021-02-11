# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime

Base = declarative_base()


class BaseTable(Base):
    __tablename__ = ''
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(120), nullable=False)
    gmt_create = Column(TIMESTAMP(True), server_default=func.now())
    gmt_modify = Column(TIMESTAMP(True), nullable=False,
                        server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return ""
