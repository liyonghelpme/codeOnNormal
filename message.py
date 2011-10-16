from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref
from stchong.model import DeclarativeBase, metadata, DBSession

class Message(DeclarativeBase):
    __tablename__ = 'message'
    uid = Column(Integer)
    mid = Column(Integer, primary_key=True)
    fid = Column(Integer) 
    mess = Column(String)
    time = Column(Integer)
    read = Column(Integer)
