from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref
from stchong.model import DeclarativeBase, metadata, DBSession

class Dragon(DeclarativeBase):
    __tablename__ = 'dragon'
    #{ Columns uid and pid can pet move from one to others ? if so pid should be independent from user 
    uid = Column(Integer)#owner
    pid = Column(Integer, primary_key=True)#pet id
    bid = Column(Integer) 
    #when move house need to update it ?take it as normal building
    #gridId = Column(Integer)#house position also means id
	#groundId = Column(Integer)#building id check from businessWrite
    
    #cityId = Column(Integer)

    friNum = Column(Integer)#how many friend help or caesars used 
    #0 not active(need friend help)
    #1 active but not buy eggs
    #2 egg 
    #3 child
    #4 young
    #5 adult
    #6 old
    #7 dead 
    state = Column(Integer)
    #egg --> 9 if feed +3  
    #check last login time diftime/24 * -1 when > 30 grow up
    #health > 0
   
    #child 25 feed+5 -1 when >= 100 
    #young +7 -2 250
    #600 dead--> -10 + 7
    health = Column(Integer)
    
    #default my pet
    name = Column(String)
    #attribute of dragon
    # no att, fire, wind, ice-cream, golden
    kind = Column(Integer)#low high  kind | clothes
    #other attribute
    #cur help friend list
    friList = Column(Integer)
    #0 not feed 1 I feed 2 friend help 3 both
    lastFeed = Column(Integer)

    attack = Column(Integer)
    trainNum = Column(Integer)
