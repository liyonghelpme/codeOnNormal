# -*- coding: utf-8 -*-
"""The application's model objects"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker,mapper
#from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import memcache
import time
import json
# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)
mc = memcache.Client(['127.0.0.1:11211'],debug=0) 
beginTime=(2011,1,1,0,0,0,0,0,0)
timestr=str(time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))
taskbonus=[]
wartaskbonus=[]
f = file('taskbonus.json')
source = f.read()
target = json.JSONDecoder().decode(source)
f2=file('wartask.json')
source2=f2.read()
if source2!=None:
    target2 = json.JSONDecoder().decode(source2)
for t in target:
    taskbonus.append([t['id'],t['des'],t['lev']])
for tt in target2:
    wartaskbonus.append([tt['id'],tt['des'],tt['lev']])

#newtask = file('newtask.json')
#newtask = newtask.read()
#newtask = json.loads(newtask)

logfile=open("logfile"+timestr,'w')
# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
# DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
#metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
######

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)
    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:

    #global t_reflected

    #t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    #mapper(Reflected, t_reflected)
    global operationaldata_table
    global useraccount_table
    global businesswrite_table
    global businessread_table
    global visitfriend_table
    operationaldata_table=Table("operationalData",metadata,autoload=True,autoload_with=engine)
    businesswrite_table=Table("businessWrite",metadata,autoload=True,autoload_with=engine)
    businessread_table=Table("businessRead",metadata,autoload=True,autoload_with=engine)
    warmap_table=Table("warMap",metadata,autoload=True,autoload_with=engine)
    map_table=Table("map",metadata,autoload=True,autoload_with=engine)
    visitfriend_table=Table("visitFriend",metadata,autoload=True,autoload_with=engine)
    ally_table=Table("ally",metadata,autoload=True,autoload_with=engine)
    victories_table=Table("victories",metadata,autoload=True,autoload_with=engine)
    gift_table=Table("gift",metadata,autoload=True,autoload_with=engine)
    occupation_table=Table("occupation",metadata,autoload=True,autoload_with=engine)
    battle_table=Table("battle",metadata,autoload=True,autoload_with=engine)
    news_table=Table("news",metadata,autoload=True,autoload_with=engine)
    friend_table=Table("friend",metadata,autoload=True,autoload_with=engine)
    friendrequest_table=Table("friendRequest",metadata,autoload=True,autoload_with=engine)
    datesurprise_table=Table("datesurprise",metadata,autoload=True,autoload_with=engine)
    datevisit_table=Table("datevisit",metadata,autoload=True,autoload_with=engine)
    card_table=Table("card",metadata,autoload=True,autoload_with=engine)
    caebuy_table=Table("caebuy",metadata,autoload=True,autoload_with=engine)
    ppyfriend_table=Table("papayafriend",metadata,autoload=True,autoload_with=engine)
    rank_table=Table("rank",metadata,autoload=True,autoload_with=engine)
   # useraccount_table=Table("userAccount",metadata,autoload=True,autoload_with=engine)
    mapper(warMap,warmap_table)
    mapper(operationalData,operationaldata_table)
    mapper(businessWrite,businesswrite_table)
    mapper(businessRead,businessread_table)
    mapper(Map,map_table)
    mapper(visitFriend,visitfriend_table)
    mapper(Ally,ally_table)
    #mapper(userAccount,useraccount_table)
    mapper(Victories,victories_table)
    mapper(Gift,gift_table)
    mapper(Occupation,occupation_table)
    mapper(Battle,battle_table)
    mapper(News,news_table)
    mapper(Friend,friend_table)
    mapper(FriendRequest,friendrequest_table)
    mapper(Datesurprise,datesurprise_table)
    mapper(Datevisit,datevisit_table)
    mapper(Card,card_table)
    mapper(Caebuy,caebuy_table)
    mapper(Papayafriend,ppyfriend_table)
    mapper(Rank,rank_table)
# Import your model modules here.
from stchong.model.auth import User, Group, Permission
from stchong.model.operationaldata import operationalData
from stchong.model.businesswrite import businessWrite
from stchong.model.ally import Ally
from stchong.model.victories import Victories
from stchong.model.gift import Gift
from stchong.model.businessread import businessRead
from stchong.model.warmap import warMap
from stchong.model.occupation import Occupation
from stchong.model.visitfriend import visitFriend
from stchong.model.map import Map
from stchong.model.battle import Battle
from stchong.model.news import News
from stchong.model.friend import Friend
from stchong.model.datesurprise import Datesurprise
from stchong.model.datevisit import Datevisit
from stchong.model.friendrequest import FriendRequest
from stchong.model.card import Card
from stchong.model.caebuy import Caebuy
from stchong.model.papayafriend import Papayafriend
from stchong.model.rank import Rank
from stchong.model.dragon import Dragon
from stchong.model.petAtt import PetAtt
from stchong.model.message import Message
from stchong.model.emptyCastal import EmptyCastal
from stchong.model.emptyResult import EmptyResult
#from stchong.model.useraccount import userAccount
