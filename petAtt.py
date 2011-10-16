from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref
from stchong.model import DeclarativeBase, metadata, DBSession

class PetAtt(DeclarativeBase):
    __tablename__ = 'petAtt'
    #{ Columns uid and piVd can pet move from one to others ? if so pid should be independent from user 
    pid = Column(Integer, primary_key=True)#pet id
    att = Column(Integer)
