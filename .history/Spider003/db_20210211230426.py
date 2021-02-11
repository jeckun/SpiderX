# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseDB:
    __tablename__ = ''
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return ""
