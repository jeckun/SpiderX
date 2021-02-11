# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseDB:
    __tablename__ = ''
