from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref
from stchong.model import DeclarativeBase, metadata, DBSession

class EmptyResult(DeclarativeBase):
    __tablename__ = 'emptyResult'
    #{ Columns uid and pid can pet move from one to others ? if so pid should be independent from user 
    eid = Column(Integer, primary_key=True)#castal id
    uid = Column(Integer)#owner -1 empty
    data = Column(String)
