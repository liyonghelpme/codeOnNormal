
from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons import response
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.exceptions import IntegrityError
from stchong.lib.base import BaseController
from stchong.model import mc,DBSession,wartaskbonus, taskbonus,metadata,operationalData,businessWrite,businessRead,warMap,Map,visitFriend,Ally,Victories,Gift,Occupation,Battle,News,Friend,Datesurprise,Datevisit,FriendRequest,Card,Caebuy,Papayafriend,Rank,logfile
from stchong import model
from stchong.controllers.secure import SecureController
from datetime import datetime
from stchong.controllers.error import ErrorController
import time
import sys
import random
import logging
import StringIO
import hashlib
import copy
import httplib
import json
__all__ = ['WarController']
class WarController(BaseController):
    @expose('json')
    def find(self, hero):
        return dict(data=hero)
    #my power and enemy power 
    #my power > enemy power win or fail
    
    #my total power ene total power pure power  1 attack 0 defence
    #return array
    # my power lost ene power lost
    def powerLost(self, poweru,powere,poweruu,poweree,type):
        lost=[0,0]
        attackLost = [[40, 50, 70, 90], [15, 20, 20, 20] ]
        defenceLost = [[35, 35, 35, 35], [20, 30, 45, 45] ]
        situation = 0
	if poweru<=2*powere:
	    situation = 0
	elif poweru>2*powere and poweru<=10*powere:
	    situation = 1
	elif poweru>10*powere and poweru<=100*powere:
	    situation = 2
	else:
	    situation = 3
        calPow = poweruu
        if poweru > powere:
            calPow = poweree
        if type==1:
            if poweru > powere:
                lost[1]=int((calPow*defenceLost[1][situation] + defenceLost[1][situation]-1)/100)#defence lost
                lost[0]=int((calPow*attackLost[1][situation] + attackLost[1][situation]-1)/100)#attack won
            else:
                lost[1]=int((calPow*defenceLost[0][situation] + defenceLost[0][situation]-1)/100)#defence lost
                lost[0]=int((calPow*attackLost[0][situation] + attackLost[0][situation]-1)/100)#attack won
        else:
            if poweru>powere:
                lost[1]=int((calPow*defenceLost[0][situation] + defenceLost[0][situation]-1)/100)#defence lost
                lost[0]=int((calPow*attackLost[0][situation] + attackLost[0][situation]-1)/100)#attack won
            else:
                lost[1]=int((calPow*defenceLost[1][situation] + defenceLost[1][situation]-1)/100)#defence lost
                lost[0]=int((calPow*attackLost[1][situation] + attackLost[1][situation]-1)/100)#attack won
        return lost        

    #occupy who in the map  occupytion
    #beoccupied by who in the map

    #battle result from operationalData and battle 
    
    #won number >= occupy victories
    #defence won >= defence won
    
    #defence number = won + lost  victories
    #attack number = attack won  attack lost 

    #won in map == occupy    victories
    #lost in map == be occupy

    #defence won in map 
    #defence lost in map  victories
    @expose('json')
    def warrecord(self,uid):
        u=checkopdata(uid)#cache
        uv=DBSession.query(Victories).filter_by(uid=int(uid)).one()
        o1=DBSession.query(Occupation).filter_by(masterid=int(uid)).all()
        a1=[]
        a2=[]
        for x in o1:
            xx=DBSession.query(operationalData.otherid,operationalData.empirename).filter_by(userid=x.slaveid).one()
            a1.append([xx.otherid,xx.empirename,1,1,x.time])
        o2=DBSession.query(Occupation).filter_by(slaveid=int(uid)).all()
        for x in o2:
            xx=DBSession.query(operationalData.otherid,operationalData.empirename).filter_by(userid=x.masterid).one()
            a2.append([xx.otherid,xx.empirename,0,0,x.time])        
        return dict(wonlist=a1,lostlist=a2,warrecord=u.battleresult,won=uv.won,dewon=uv.dewon,defence=uv.dewon+uv.delost,attack=uv.won+uv.lost,woninmap=uv.woninmap,lostinmap=uv.lostinmap,dewoninmap=uv.dewoninmap,delostinmap=uv.delostinmap)                                                        
