# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Float, Integer, String, Text, Date, DateTime

Base = declarative_base()


class BaseDB:
    __tablename__ = ''
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return ""
