# -*- coding: utf-8 -*-
"""Main Controller"""


from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons import response
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sqlalchemy import sql
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_, desc, select
from sqlalchemy import func
from stchong.lib.base import BaseController
from stchong.model import mc,DBSession,wartaskbonus, taskbonus,metadata,operationalData,businessWrite,businessRead,warMap,Map,visitFriend,Ally,Victories,Gift,Occupation,Battle,News,Friend,Datesurprise,Datevisit,FriendRequest,Card,Caebuy,Papayafriend,Rank
from stchong.model import Dragon
from stchong.model import Message
from stchong.model import PetAtt
from stchong.model import EmptyCastal
from stchong.model import EmptyResult
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
import inspect
__all__ = ['RootController']
class RootController(BaseController):
    secc = SecureController()
    global getCity
    
    global accCost
    global Plant_Price#农作牨
    global beginTime#2011年1月1日0时0分常量
    global houses#民居生产列表
    global soldie#士兵列表
    global soldiernum#士兵经验
    global production#商业列表
    global read#read内部函数
    global mapKind#地图种类对应最大用户数列表
    global makeMap#内部函数，新建地图
    global insert#内部函数，增加warmap中num数
    global getMap#内部函数，获取类型为kind的有空位的地图
    global upd#内部函数，从旧地图升级到新地图
    global housebuild#民居建筑列表
    global resourcebuild#资源建筑物列表
    global milbuild#军事建筑物列表
    global businessbuild#商业建筑物列表
    global godbuild#神像建筑物列表
    global statuebuilding#雕��
    global decorationbuild#装饰列表
    global specialgoods#内部函数，判断建筑物特殊物品是否得到满足
    global getGround_id#内部函数,返回建筑物id对应列表
    global stones#石头种类列表
    global woods#木头种类列表
    global expanding#扩地列表
    global EXPANDLEV#扩地最高等级
    global getbonus#内部函数，打怪奖励
    global loginBonus#内部函数，登录奖励
    global alphabet#特殊物品对应字母列表a-l
    global randombuilding#没有被使用，随机一级建筑物列表
    global present#没有被使用，内部函数
    global inornot#内部函数，判断整数是否在列表内
    global allyup#每个爵位等级默认初始拥有最多盟友数
    global NOBILITYUP#爵位最高等级0-6
    global INITIALSTR#没有被使用，初始化字符串
    global INITIALSTR2#正在使用，初始化字符串
    global loginbonuslist#登录奖励列表，连续登录奖励
    global timejudge #内部函数，判断时间是否相差一天function pan duan shifou duguo 0 dian 
    global giftstring #内部函数，返回用户相关礼物字符串 function giftstring
    global sg#内部函数，赠送特殊物品作为礼物
    global minusstateeli#内部函数，消除负面状态function eliminating minusstate
    global completereceive#内部函数，完成礼物赠予或收取
    global checkminusstate#内部函数，查询负面状态是否存在
    global monsterlist#怪物列表
    global returnSoldier#内部函数，返回士兵数量
    global returnsentouryoku#内部函数，返回城内战斗力
    global checkopdata#function,cache
    global deleteopdata#function,cache
    global returnscout#内部函数，返回侦察兵数量function,return scout num of user
    global defencepowerlist#每一级城堡防御力list of defence power of each nobility
    global allyhelp#内部函数返回盟友提供战力function ally help
    global getbonusbattle#内部函数，返回战斗奖励functionspecialgoods bonus for battle
    global warresult#内部函数，返回战争结果function  calculate result of battles
    global functionname#函数名列表list of function name
    global calev#内部函数，计算爵位等级function castle lev up
    global addnews#内部函数，新闻function add news
    global opentreasurebox#内部函数，计算打开宝箱奖励function
    global nobilitybonuslist#爵位升级奖励
    global tasklist#任务列表
    #global newtask#内部函数，新任务
    global mktaskstr#内部函数，计算任务字符串
    global checkfriend#内部函数，检查是否在好友列表中
    global md5string#计算md5用string
    global judgemd5#内部函数，计算md5
    global CACHEOP#常量，cache调用次数。
    global addcache#内部函数，向cache中写入数据
    global replacecache#内部函数
    global cachewriteback#内部函数
    global callost#内部函数，计算损失
    global getresource
    global warresult2
    global calGod
    global getbonusbattle2
    global defenceplist
    global appsecret
    global tasknew
    global tasknew3
    global SERVER_NAME
    global wartasknew#战争任务
    global checkprotect#检查保护
    global recalev#计算爵位等级差
    global battlebonus#战争时根据爵位获得奖励
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    #housebuild：corn,food,resource(+:m -:s),快速升级cae,exp,time，特殊物品，解锁等级
    housebuild=[[500,10,0,0,3,600,None,1],[1400,30,0,1,8,1200,'a,1',1],[2800,0,70,2,15,2400,'a,2;b,3',1],[int(500*1.1),10,0,0,3,600,None,1],[int(1400*1.1),30,0,1,8,1200,'a,1',1],[int(2800*1.1),0,70,2,15,2400,'a,2;b,3',1],[int(500*1.2),10,0,0,3,600,None,1],[int(1400*1.2),30,0,1,8,1200,'a,1',1],[int(2800*1.2),0,70,2,15,2400,'a,2;b,3',1],[int(500*1.3),10,0,0,3,600,None,1],[int(1400*1.3),30,0,1,8,1200,'a,1',1],[int(2800*1.3),0,70,2,15,2400,'a,2;b,3',1],[1500,60,0,0,5,1800,None,5],[4800,120,0,3,13,4800,'b,2;c,2',5],[9000,0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.1),60,0,0,5,1800,None,5],[int(4800*1.1),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.1),0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.2),60,0,0,5,1800,None,5],[int(4800*1.2),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.2),0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.3),60,0,0,5,1800,None,5],[int(4800*1.3),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.3),0,100,4,24,9000,'c,2;d,3',5],[7300,400,0,0,13,15840,None,10],[15000,0,150,4,21,24480,'f,2;g,2',10],[19000,0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.1),400,0,0,13,15840,None,10],[int(15000*1.1),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.1),0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.2),400,0,0,13,15840,None,10],[int(15000*1.2),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.2),0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.3),400,0,0,13,15840,None,10],[int(15000*1.3),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.3),0,-150,5,30,30600,'g,2;h,3',10],[3500,200,0,0,11,5400,None,15],[6600,0,120,5,25,11160,'d,2;e,2',15],[11000,0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.1),200,0,0,11,5400,None,15],[int(6600*1.1),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.1),0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.2),200,0,0,11,5400,None,15],[int(6600*1.2),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.2),0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.3),200,0,0,11,5400,None,15],[int(6600*1.3),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.3),0,-120,6,39,21240,'e,2;f,3',15],[10500,600,0,0,20,25200,None,20],[15500,0,200,7,32,36720,'h,2;i,2',20],[19500,0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.1),600,0,0,20,25200,None,20],[int(15500*1.1),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.1),0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.2),600,0,0,20,25200,None,20],[int(15500*1.2),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.2),0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.3),600,0,0,20,25200,None,20],[int(15500*1.3),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.3),0,-200,8,43,71640,'i,2;j,2',20],[-10,0,0,0,15,7560,None,5],[20000,0,300,12,25,15480,'b,2;c,2',5],[25000,0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.1),0,0,0,15,7560,None,5],[int(20000*1.1),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.1),0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.2),0,0,0,15,7560,None,5],[int(20000*1.2),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.2),0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.3),0,0,0,15,7560,None,5],[int(20000*1.3),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.3),0,-300,15,40,30600,'c,2;d,3',5],[-8,0,0,0,20,12240,None,3],[22000,0,310,15,30,19800,'a,2;f,2',3],[26000,0,-310,20,50,28800,'d,2;i,4',3],[int(-9),0,0,0,20,12240,None,3],[int(1.1*22000),0,310,15,30,19800,'a,2;f,2',3],[int(1.1*26000),0,-310,20,50,28800,'d,2;i,4',3]]#corn,food,resource(+:m -:s),快速升级cae,exp,time，特殊物品，解锁等级corn,food,resource(+:m -:s),cae,exp,time
    #resourcebuild：corn,food,labor_num,wood,exps，解锁等级
    resourcebuild=[[1000,0,80,0,5,0],[-10,0,0,0,15,10],[-15,0,0,0,40,20],[-20,0,0,0,70,30],[10000,600,120,0,20,10],[28500,1000,250,0,30,18]]#corn,food,labor_num,wood,exps
    #milbuild：corn,food,labor_num,resource,update(cae),exp,time，特殊物品，解锁等级
    milbuild=[[4000,130,100,0,0,5,3600,None,1],[9000,0,20,200,5,10,11520,'a,3',1],[20000,0,50,-200,10,20,22680,'b,3;c,4',1],[12000,320,130,0,0,15,7200,None,5],[25000,0,20,500,7,20,14760,'b,3',5],[50000,0,50,-500,15,35,28440,'c,3;d,4',5],[6000,150,90,0,0,7,10800,None,5],[12000,0,20,300,3,15,21600,'c,3',5],[25000,0,50,-300,7,30,32400,'d,3;e,4',5]]#corn,food,labor_num,resource,update(cae),exp,time
    #businessbuild：corn,food,labor,resource,update(cae),exp,time，特殊物品，解锁等级
    businessbuild=[[300,20,20,0,0,3,600,None,1],[500,30,5,0,1,7,1800,'a,1',1],[1100,0,10,70,2,11,3600,'a,2;b,3',1],[1200,45,40,0,0,5,3600,None,4],[1800,50,10,100,3,9,10740,'b,2;c,2',4],[3000,70,15,-100,4,14,15120,'c,2;d,3',4],[-5,0,0,0,0,15,5400,None,6],[5000,0,0,120,6,20,14400,'b,2;c,2',6],[7000,0,0,-120,7,25,23400,'c,2;d,3',6],[2000,80,50,0,0,7,19800,None,8],[3300,0,15,150,5,9,35270,'d,2;e,2',8],[4500,0,20,-150,6,11,46800,'e,2;f,3',8],[5000,100,70,0,0,9,8280,None,15],[7000,0,20,170,7,11,22320,'f,2;g,2',15],[13500,0,25,-170,8,13,28800,'g,2;h,3',15],[-8,0,0,0,0,25,20520,None,14],[9000,130,0,200,10,30,25200,'d,2;e,2',14],[11000,0,0,-200,11,35,33120,'e,2;f,3',14],[7200,130,90,0,0,20,21600,None,21],[11000,0,25,210,9,33,28800,'h,2;i,2',21],[19900,0,30,-210,10,45,36720,'i,2;j,3',21],[8000,170,110,0,0,29,30600,None,29],[13000,0,30,230,10,45,34200,'j,2;k,2',29],[21000,0,35,-230,11,61,46800,'k,2;l,3',29],[-11,0,0,0,0,35,25200,None,24],[13000,0,0,250,12,45,30240,'h,2;i,2',24],[17000,0,0,-250,13,60,39600,'i,2;j,3',24],[10000,1000,55,0,0,8,16200,None,7],[20000,0,18,300,7,15,28800,'a,5;i,4',7],[50000,0,27,-300,10,25,41400,'c,5;d,6',7]]#corn,food,labor,resource,update(cae),exp,time
    #godbuild corn,food,升级cae,exp,人口上限populationupbound，时间
    godbuild=[[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[20000,1000,5,100,250,21600],[20000,1000,5,100,250,21600],[20000,1000,5,100,250,21600],[20000,1000,5,100,250,21600],[50000,2000,10,170,250,43200],[50000,2000,10,170,250,43200],[50000,2000,10,170,250,43200],[50000,2000,10,170,250,43200],[100000,5000,15,250,250,64800],[100000,5000,15,250,250,64800],[100000,5000,15,250,250,64800],[100000,5000,15,250,250,64800],[500000,10000,30,350,250,86400],[500000,10000,30,350,250,86400],[500000,10000,30,350,250,86400],[500000,10000,30,350,250,86400]]# corn,food,cae,exp,populationupbound
    #statuebuilding lev,corn(cae) defenceadd pop time
    statuebuilding = [[27,80000,600,20,7200],[30,-8,700,40,14400],[32,120000,950,80,21600],[34,-12,1200,60,28800],[37,200000,1600,120,36000],[40,-20,2500,100,43200]]
    #decorationbuild：cornorcae，人口上限，解锁等级
    decorationbuild=[[10,5,1],[20,5,1],[30,5,1],[50,5,4],[-1,50,5],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[200,8,7],[-3,170,8],[400,15,9],[600,20,10],[800,25,11],[1000,30,12],[900,35,13],[1200,40,14],[2000,50,15],[-5,300,10],[1500,60,16],[1500,60,16],[1500,60,16],[1600,65,18],[1600,65,18],[1600,65,18],[1600,65,18],[-3,150,15],[-3,150,15],[-3,150,15],[-3,150,15],[1800,70,20],[1800,70,20],[1800,70,20],[2000,80,25],[2000,80,25],[2000,80,25],[-10,300,20],[5000,90,3],[-5,150,3],[-10,300,3],[2000,30,17],[2000,30,17],[-10,300,20]]#corn(or cae),populationupbound
    #农作物list：#corn,exp,food,time，解锁等级
    Plant_Price=[[50,1,20,600,1],[165,3,50,2700,1],[-1,8,120,3600,5],[700,7,150,9360,5],[1440,12,300,22680,7],[-3,25,430,14400,7],[230,5,52,1800,13],[600,9,80,5400,16],[-2,30,280,9000,10],[1210,15,200,11520,20],[3000,25,410,29160,25],[-5,50,650,25200,15]]#corn,food,cae
    beginTime=(2011,1,1,0,0,0,0,0,0)
    #人口招募 招募人口数population,消耗food,exp got,cae（不用） 
    houses=[[10,20,1,1800,1],[15,30,2,1800,1],[20,40,5,1800,1],[10,20,1,1800,1],[15,30,2,1800,1],[20,40,5,1800,1],[10,20,1,1800,1],[15,30,2,1800,1],[20,40,5,1800,1],[10,20,1,1800,1],[15,30,2,1800,1],[20,40,5,1800,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[50,90,6,12600,2],[62,116,10,12600,3],[75,142,17,12600,3],[50,90,6,12600,2],[62,116,10,12600,3],[75,142,17,12600,3],[50,90,6,12600,2],[62,116,10,12600,3],[75,142,17,12600,3],[50,90,6,12600,2],[62,116,10,12600,3],[75,142,17,12600,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[100,150,15,14400,4],[150,225,25,14400,4],[200,300,35,14400,4],[100,150,15,14400,4],[150,225,25,14400,4],[200,300,35,14400,4],[100,150,15,14400,4],[150,225,25,14400,4],[200,300,35,14400,4],[100,150,15,14400,4],[150,225,25,14400,4],[200,300,35,14400,4],[110,170,17,21600,0],[165,245,26,21600,0],[230,339,39,21600,0],[110,170,17,21600,0],[165,245,26,21600,0],[230,339,39,21600,0]]##人口招募 招募人口数population,消耗food,exp got,cae（不用） 
    #士兵：corn,food,labor_num,cae（不要），时间
    soldie=[[750,90,30,3,7200],[2400,270,90,3,21600],[4800,540,180,3,43200],[1600,180,30,3,7200],[5000,540,90,3,21600],[10000,1080,180,3,43200],[2400,270,30,3,7200],[7500,810,90,3,21600],[15000,1620,180,3,43200],[2000,150,15,6,7200],[6300,450,45,6,21600],[12600,900,90,6,43200],[2600,300,15,6,7200],[7900,900,45,6,21600],[15800,1800,90,6,43200],[3300,450,15,6,7200],[10000,1350,45,6,21600],[20000,2700,90,6,43200],[150,10,2,9,7200],[500,30,6,9,21600],[1000,60,12,9,43200],[310,20,2,9,7200],[990,60,6,9,21600],[1980,120,12,9,43200],[480,30,2,9,7200],[1500,90,6,9,21600],[3000,180,12,9,43200]]#corn,food,labor_num,cae
    #士兵经验
    soldiernum=[5,8,13,9,15,21,16,25,34,10,15,20,30,40,50,60,75,90,3,6,9,5,8,13,9,15,21]#soldier exp
    #商业生产 产量，经验，cae（不要），时间
    production=[[100,1,1,600],[300,2,1,600],[500,5,1,600],[600,3,1,5400],[900,5,1,5400],[1200,9,1,5400],[800,5,2,1800],[1400,9,2,1800],[2100,15,2,1800],[1200,5,1,10440],[1800,9,1,10440],[2600,17,1,10440],[2300,12,2,21600],[3200,20,2,21600],[4500,29,2,21600],[2500,18,3,7200],[4400,28,3,7200],[6800,40,3,7200],[1400,10,2,11160],[2100,19,2,11160],[3100,30,2,11160],[3500,23,3,30600],[6500,34,3,30600],[8000,45,3,30600],[7500,30,12,26200],[13000,50,12,26200],[17500,70,12,26200],[1800,4,0,16200],[2600,8,0,16200],[4400,12,0,16200]]#corn that the plant can produce for a cycle,production,exp,speedup cae 
    #扩地list 金钱，cae币
    expanding=[[10000,1,10],[50000,3,20],[100000,5,50],[500000,7,90],[1000000,10,140],[1500000,15,200],[2000000,20,330],[2500000,27,580],[3000000,37,740],[5000000,50,920]]#ing land corn,cae
    error = ErrorController()
    EXPANDLEV=10#最高等级 ，从0开始
    #不使用randombuilding
    randombuilding=[[1,1],[100,1],[103,5],[106,10],[109,15],[112,20],[300,1],[303,5],[309,10],[312,15],[318,20],[321,25],[500,1],[501,1],[502,1],[503,1],[505,1],[508,5],[509,5],[510,5],[511,5],[512,5],[513,5],[514,7],[515,8],[516,9],[519,13],[520,14],[521,15],[522,16],[523,17],[525,19],[526,19],[527,19],[528,19],[529,20],[530,20],[531,20],[536,22],[537,22],[538,22],[539,23],[541,24]]#building id, lev
    #各爵位地图用户数
    mapKind=[8,32,72,128,200,512,800]
    #woods product cost(corn or cae),exp,gain,time，解锁等级
    woods=[[600,5,20,4320,7],[1850,15,50,21600,10],[-4,20,70,6480,7],[1000,10,40,5400,15],[2500,20,80,25200,20],[-8,50,120,9000,7]]#woods product cost(corn or cae),exp,gain,time
    #stones product cost(corn or cae),exp,gain,time，解锁等级
    stones=[[1200,10,20,4320,10],[3600,20,50,21600,15],[-5,30,70,6480,10],[2000,15,40,5400,20],[5500,25,80,25200,25],[-10,65,120,9000,10]]#stones product cost(corn or cae),exp,gain,time
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n']
    allyup=[1,2,3,4,5,6,7]
    loginbonuslist=[3000,5000,8000,12000,-2]#loginbonus
    #怪兽list 战斗力，经验，corn，随机物品数量，损失战斗力
    monsterlist=[20,30,41,25,37,49,28,42,56,33,49,65,40,58,77,50,75,100,42,65,90,51,74,104,60,90,120,73,109,145,80,120,160,100,150,200]#50,60,90,100,40,50,100,110,180,200]
    #monsterlist=[[50,10,1700,1,28],[100,30,3100,1,55],[150,50,4600,2,83],[200,80,6000,2,110],[300,110,8900,2,165],[500,150,15000,3,275],[1000,200,30000,3,550]]
    INITIALSTR="0,782,0,0,1;501,818,-1,0,1;516,824,-1,0,1;525,825,-1,0,1;501,858,-1,0,1;534,859,-1,0,1;100,863,-1,0,1;517,864,-1,0,1;526,865,-1,0,1;501,895,-1,0,1;501,896,-1,0,1;501,897,-1,0,1;501,898,-1,0,1;501,899,-1,0,1;501,900,-1,0,1;501,901,-1,0,1;501,902,-1,0,1;501,903,-1,0,1;501,904,-1,0,1;501,905,-1,0,1;501,906,-1,0,1;501,938,-1,0,1;501,978,-1,0,1;300,980,-1,1,1;1,983,-1,0,1;1,985,1,1,1;200,857,-1,"
    INITIALSTR2="0,455,0,0,1;503,491,-1,0,1;503,527,-1,0,1;503,531,-1,0,1;503,528,-1,0,1;503,567,-1,0,1;520,568,-1,0,1;503,571,-1,0,1;503,606,-1,0,1;503,607,-1,0,1;503,608,-1,0,1;503,609,-1,0,1;503,610,-1,0,1;503,611,-1,0,1;503,612,-1,0,1;503,613,-1,0,1;503,614,-1,0,1;503,615,-1,0,1;503,616,-1,0,1;530,646,-1,0,1;503,651,-1,0,1;1,688,-1,0,1;503,691,-1,0,1;503,731,-1,0,1;503,771,-1,0,1;200,566,-1,"
    NOBILITYUP=6 
    #defencepower,corn,food,wood,stone,cae
    defencepowerlist=[[50,10000,500,0,0,5],[100,20000,1000,0,0,5],[200,50000,0,500,0,20],[500,150000,0,500,500,50],[700,200000,0,1000,1000,70],[1000,250000,0,1500,1500,100],[5000,1000000,0,5000,5000,500]]#defencepower,corn,food,wood,stone,cae
    #defencepower,cae,food,stone,wood
    defenceplist=[[100,5,10,0,0],[300,13,10,0,0],[500,21,0,0,5],[700,29,0,0,5],[1000,42,0,5,0],[3000,110,0,5,0],[5000,188,0,5,0]]
    functionname=['logsign','retlev','build','planting','harvest']
    #corn,food,wood,stone
    nobilitybonuslist=[[5000,250,0,0],[10000,500,0,0],[30000,1500,0,0],[50000,2500,0,0],[70000,3500,0,0],[100000,5000,0,0]]
    battlebonus=[[5000,6000,7000],[7000,8000,9000],[10000,12000,14000],[14000,16000,18000],[20000,23000,25000],[25000,27000,29000],[50000,50000,50000]]#nobility,subno
    md5string='0800717193'
    log=logging.getLogger('root')
    CACHEOP=10#调用10次checkopdata
    appsecret='FA6AMZKT77L4e4bc0a6'
    SERVER_NAME = "cn.papayamobile.com"
    #任务列表
    tasklist=[[['查看帮助文档','不耻下问是良好美德，点击Menu键（或设置图标）查看帮助文档~','查看帮助文档 0/1',100,5,'0,0'],['种植粮食','地主家也没有余粮了，伤不起呀！快去种点啥吧，，','开垦农田 0/1;种植胡萝卜 0/6',300,10,'1,1!0$1','2,1!0$6'],['店铺收税','咱也是地主啦！快去店铺收税吧','普通面包房收税 0/250',100,5,'2,100!0$250']]]
    @expose('json')
    def share(self,uid):
        u=checkopdata(uid)
        u.corn=u.corn+100
        replacecache(uid,u)
        return dict(id=1)
    def judgemd5(string,md5s):
        src=string+'-'+md5string
        md5=hashlib.md5(src).hexdigest()
        if md5==md5s:
            return True
        else:
            return False
    @expose('json')
    def getOtherid(self, uid):
        try:
            user = checkopdata(uid)
        except:
            return dict(id=0, reason='no such user')
        return dict(id=1, otherid=user.otherid)
    @expose('json')
    def removeMsg(self, uid, mid):
        msg = DBSession.query(Message).filter_by(mid=mid).one()
        DBSession.delete(msg)
        return dict(id=1, result="remove suc")
    @expose('json')
    def sendMsg(self, uid, fid, msg):
        uid = int(uid)
        fid = int(fid)
        if fid == 2800:#sendMsg caesar to xiongge
            fid = 2736
        cur = int(time.mktime(time.localtime()) - time.mktime(beginTime))
        msg = Message(uid=uid, fid=fid, mess = msg, read = 0, time=cur)
        DBSession.add(msg)
        return dict(id=1, result="send msg suc")

    @expose('json')
    def fetchMsg(self, uid, start, end):
        uid = int(uid)
        start = int(start)
        end = int(end)
        nums = DBSession.query(Message).filter_by(fid=uid).count()
        print "msg num " + str(uid) +' '+str(nums)
        if start > nums:
            return dict(id=0, leftNum = 0, reason = "no more unread msg")
        if start < 0:
            start = 0
        if end > nums:
            end = nums

        if end == -1:
            end = nums
            msgs = DBSession.query(Message.mid, Message.uid, Message.mess, Message.time, Message.read, operationalData.otherid).filter_by(fid=uid).filter(Message.uid==operationalData.userid).order_by(desc(Message.time)).slice(start, nums).all()
        else:
            msgs = DBSession.query(Message.mid, Message.uid, Message.mess, Message.time, Message.read, operationalData.otherid).filter_by(fid=uid).filter(Message.uid==operationalData.userid).order_by(desc(Message.time)).slice(start, end).all()
        for m in msgs:
           #print str(m)
            ms = DBSession.query(Message).filter_by(mid=m[0]).one()
            ms.read = 1
        DBSession.flush()
        return dict(id=1, leftNum = nums-end, msg = msgs)

    @expose('json')
    def completepay(self,uid,tid,papapas,signature):
        u=checkopdata(uid)
        ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
        caeplus=0
        reward = [1, 5, 15, 40]
        if u.tid=='-1':
            s=hashlib.md5(u.otherid+'-'+tid+'-'+appsecret).hexdigest()
            cb=u.cae
            if s==signature:
                u.paytime=-1
                if int(papapas)==300:
                    u.cae=u.cae+int(int(papapas)/100)
                    caeplus=int(int(papapas)/100)
                elif int(papapas)==1000:
                    u.cae=u.cae+10+reward[0]
                    caeplus=10+reward[0]
                elif int(papapas)==2500:
                    u.cae=u.cae+25+reward[1]
                    caeplus=25+reward[1]
                elif int(papapas)==5000:
                    u.cae=u.cae+50+reward[2]
                    caeplus=50+reward[2]
                elif int(papapas)==10000:
                    u.cae=u.cae+100+reward[3]
                    caeplus=100+reward[3]
                else:
                    u.cae=u.cae+int(int(papapas)/100)
                ca=u.cae
                try:
                    x=DBSession.query(Caebuy).filter_by(uid=u.userid).filter_by(time=ti).one()
                    x.cae=int(int(papapas)/100)
                except:
                    ncb=Caebuy(uid=u.userid,cae=int(int(papapas)/100),time=ti)
                    #return dict(ti=ti)
                    DBSession.add(ncb)
                return dict(id=1)
            else:
                return dict(id=0)
        else:
            if tid!=u.tid:
                return dict(id=0)
            u.tid='-1'
            u.paytime=-1
            u.cae=u.cae+int(int(papapas)/100)
            ca=u.cae
            try:
                x=DBSession.query(Caebuy).filter_by(uid=u.userid).filter_by(time=ti).one()
                x.cae=caeplus
            except:
                ncb=Caebuy(uid=u.userid,cae=caeplus,time=ti)
                DBSession.add(ncb)            
            print inspect.stack()[0]
            return dict(id=1)
    #######payment
    @expose()
    def payment(self,tid,uid,papapas,signature,time):
        try:
            uu=DBSession.query(operationalData).filter_by(otherid=uid).filter_by(user_kind=0).one()
            DBSession.commit()
            u=checkopdata(uu.userid)
            s=hashlib.md5(tid+'-'+uid+'-'+papapas+'-'+appsecret).hexdigest() 
            if s==signature:
                return '1'
            else:
                return '0'
        except:
            return '0'
    ###########iphone 邀请好友相关
    @expose('json')
    def sethead(self,hid,uid):
        u=checkopdata(uid)
        u.hid=int(hid)
        replacecache(uid,u)
        return dict(id=1)
    @expose('json')
    def sendinvite(self,uid,invitestring):
        try:
            uu=DBSession.query(operationalData).filter_by(userid=int(invitestring)).one()
            DBSession.commit()
            u=checkopdata(uu.userid)
            ub=checkopdata(uid)
            if u.invite==1 or ub.invited==1:
                return dict(id=0)
            ub.invited=1
            u.invite=1
            u.inviteid=ub.userid
            u.cae=u.cae+3
            print inspect.stack()[0]
            try:
                f=DBSession.query(Friend).filter_by(uid=uid).filter_by(fotherid=fotherid).one()            
                DBSession.commit()
            except:
                nf=Friend(uid=uid,fotherid=u.otherid)
                DBSession.add(nf)
                DBSession.commit()
                nf2=Friend(uid=u.userid,fotherid=ub.otherid)
                DBSession.add(nf2)
                DBSession.commit()
            replacecache(u.userid,u)
            replacecache(uid,ub)
            return dict(id=1)
        except:
            return dict(id=0)
    @expose('json')
    def invitefriend(self,uid,fid):
        uid=int(uid)
        fid=int(fid)
        try:
            #uf=DBSession.query(operationalData).filter_by(userid=fid).one()
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            uf=checkopdata(fid)#cache
            u=checkopdata(uid)#cache
            istring=''
            istring=u.empirename+','+str(u.lev)+','+str(u.nobility)
            if uf.invitestring=='' or uf.invitestring==None:
                uf.invitestring=istring
            else:
                uf.invitestring=uf.invitestring+';'+istring
            replacecache(fid,uf)#cache
            #replacecache(uid,u)
            return 2
        except:
            return dict(id=0)
    @expose('json')
    def acceptfriend(self,uid,fotherid,user_kind):
        uid=int(uid)
        user_kind=int(user_kind)
        try:
            f=DBSession.query(Friend).filter_by(uid=uid).filter_by(fotherid=fotherid).one()
            return dict(id=0)
        except InvalidRequestError:
            nf=Friend(uid=uid,fotherid=fotherid)
            DBSession.add(nf)
            uf1=DBSession.query(operationalData).filter_by(otherid=fotherid).filter_by(user_kind=1).one()
            uf=checkopdata(uf1.userid)#cache
            u=checkopdata(uid)#cache
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            nf2=Friend(uid=uf.userid,fotherid=u.otherid)
            try:
                fr=DBSession.query(FriendRequest).filter_by(sendid=fotherid).filter_by(receiveid=u.otherid).one()
                fr.delete()
            except:
                x=1
            DBSession.add(nf2)
            return dict(id=1) 
    @expose('json')
    def refusefriend(self,uid,fotherid,user_kind):
        uid=int(uid)
        user_kind=int(user_kind)
        try:
            fr=DBSession.query(FriendRequest).filter_by(sendid=fotherid).filter_by(receiveid=u.otherid).one()
            fr.delete()
            return dict(id=1)
        except:
            x=1
            return dict(id=1)            
    @expose('json')
    def makefriend(self,uid,fotherid,user_kind,message):
        uid=int(uid)
        user_kind=int(user_kind)
        u=checkopdata(uid)
        nfr=RequestFriend(sendid=u.otherid,receiveid=fotherid,message=message)
        DBSession.add(nfr)
        return dict(id=1)
    @expose('json')
    def returnrequest(self,uid):
        u=checkopdata(uid)
        rlist=[]
        d=DBSession.query(FriendRequest).filter_by(receiveid=u.otherid)
        
        for x in d:
            u=DBSession.query(operationalData).filter_by(otherid=x.otherid).filter_by(user_kind=1).one()
            rlist.append([x.sendid,x.message,x.hid,x.empirename])
        return dict(requestlist=rlist)
    @expose('json')
    def returnfriendlist(self,uid):
        uid=int(uid)
        friendlist=[]
        try:
            fset=DBSession.query(Friend).filter_by(uid=uid)
            for n in fset:
                u=DBSession.query(operationalData).filter_by(otherid=n.fotherid).filter_by(user_kind=1).one()
                friendlist.append([n.fotherid,u.empirename,u.hid])
                
            return dict(friendlist=friendlist)
        except:
            return dict(id=0)
    def checkfriend(uid,fotherid):
        uid=int(uid)
        try:
            fs=DBSession.query(Friend).filter_by(uid=uid)
            for f in fs:
                if f.fotherid==fotherid:
                    return False
            return True
        except:
            return True
    @expose('json')
    def refreshfriend(self,uid,page):
        uid=int(uid)
        userlist=[]
        nl=[]
        num=5
        x=0 
        page=int(page)  
        friendlist=[]     
        try:
            userset=DBSession.query(operationalData).filter_by(user_kind=1).order_by(operationalData.userid)#是否只能要求iphone版好友？
            for nn in userset:
                n=checkopdata(nn.userid)#cache
                if checkfriend(uid,n.otherid)==True:
                    if n.userid!=uid:
                        ntemp=[n.otherid,n.userid,n.empirename,n.lev,n.nobility,n.hid]
                        nl.append(ntemp)    
            if len(nl)==0 or nl==None :
                return dict(id=0)
            if len(nl)-1<page*num:
                return dict(id=0)
            l1=0
            if len(nl)>(page+1)*num:
                l1=(page+1)*num+1
            else:
                l1=len(nl)
            i=page*num
            while i<l1:               
                friendlist.append(znl[i])
                i=i+1
            #return dict(id=1)
            return dict(refreshfriend=friendlist)
                
        except InvalidRequestError:
            return dict(id=0)         
    ###########任务相关
    @expose('json')
    def newtasktest(self,uid):#测试用，创建新任务
        u=None
        tl=None
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            #tl=newtask(u)
            replacecache(uid,u)#cache
            return dict(tasklist=tl)
        except:
            return dict(id=tl)
    @expose('json')
    def wartaskgivenup(self,uid):#放弃任务
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        #tasklist=newtask(u) 
        
        
        u.wartaskstring=''     
        #u.wartasknum=u.wartasknum+1
        task=wartasknew(uid)
        u.warcurrenttask=task[1]
        u.wartaskstring='0'
        replacecache(uid,u)#cache
        if task[0]<0:
            return dict(task=-1)
        return dict(task=task[0])    
    @expose('json')
    def taskgivenup(self,uid):#放弃任务
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        #tasklist=newtask(u) 
        
        
        u.taskstring=''     
        u.tasknum=u.tasknum+1
        task=tasknew(uid)
        u.currenttask=task[1]
        u.taskstring='0'
        replacecache(uid,u)#cache
        if task[0]<0:
            return dict(task=-1)
        return dict(task=task[0])
    @expose('json')
    def wartaskaccomplished(self,uid):#任务完成
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        if u.warcurrenttask==None or u.warcurrenttask=='' or int(u.warcurrenttask)<0 or int(u.warcurrenttask)>len(taskbonus)-1:
            return dict(task=-1)
        u.corn=u.corn+wartaskbonus[int(u.warcurrenttask)][1][0]
        u.exp=u.exp+wartaskbonus[int(u.warcurrenttask)][1][1]  
        t=wartasknew(uid)   
        task=t[0]
        t2=t[1]
        u.wartaskstring='' 
        u.warcurrenttask=t2   
        u.wartaskstring='0'
        #tasklist1=newtask(u)
        replacecache(uid,u)#cache
        if task<0:
            task=-1
        return dict(task=task,tid=t2)         
    @expose('json')
    def taskaccomplished(self,uid):#任务完成
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        if u.currenttask==None or u.currenttask=='' or int(u.currenttask)<0 or int(u.currenttask)>len(taskbonus)-1:
            return dict(task=-1)
        u.corn=u.corn+taskbonus[int(u.currenttask)][1][0]
        u.exp=u.exp+taskbonus[int(u.currenttask)][1][1]  
        t=tasknew(uid)   
        task=t[0]
        t2=t[1]
        u.taskstring='' 
        u.currenttask=t2   
        u.taskstring='0'
        #tasklist1=newtask(u)
        replacecache(uid,u)#cache
        if task<0:
            task=-1
        return dict(task=task,tid=t2) 
    @expose('json')
    def wartaskstep(self,uid,taskstring):#任务中间步骤完成保存
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.wartaskstring=taskstring
        replacecache(uid,u)#cache
        return dict(id=1)        
    @expose('json')
    def taskstep(self,uid,taskstring):#任务中间步骤完成保存
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.taskstring=taskstring
        replacecache(uid,u)#cache
        return dict(id=1)
    @expose('json')
    def tasknew2(self,uid):
        u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus):
                return -1
            else:
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:
                    u.currenttask=str(-int(u.currenttask))
                    return dict(id=u.currenttask)
                u.currenttask=str(ct+1)
                u.taskstring='0'
                replacecache(uid,u)
                return dict(ct=ct,t=u.currenttask,tid=taskbonus[ct+1][0])  
    def wartasknew(uid):
        u=checkopdata(uid)
        if u.warcurrenttask=='-1' or u.warcurrenttask=='':
            u.warcurrenttask=str(0)
            u.wartaskstring='0'
            replacecache(uid,u)
            return [wartaskbonus[0][0],0]
        else:
            if int(u.warcurrenttask)>=len(wartaskbonus)-1 or int(u.warcurrenttask)<=(-len(wartaskbonus)+1):
                u.warcurrenttask=str(-int(u.warcurrenttask))
                u.wartaskstring=''
                replacecache(uid,u)
                return [-1,u.warcurrenttask]
            else:
                if int(u.warcurrenttask)<0:
                    u.warcurrenttask=str(-int(u.warcurrenttask))
                ct=int(u.warcurrenttask)
                #if taskbonus[ct+1][2]>u.lev:
                #    u.warcurrenttask=str(-int(u.warcurrenttask))
                #    replacecache(uid,u)
                #    return [-1,u.warcurrenttask]
                u.warcurrenttask=str(int(u.warcurrenttask)+1)
                u.wartaskstring='0'
                replacecache(uid,u)
                return [wartaskbonus[ct+1][0],u.warcurrenttask]                  
    #no task 0 just add a task at position
    def tasknew(uid):
        u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus)-1 or int(u.currenttask)<=(-len(taskbonus)+1):
                u.currenttask=str(-int(u.currenttask))
                u.taskstring=''
                replacecache(uid,u)
                return [-1,u.currenttask]
            else:#level is ok
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:#level not satisfied
                    u.currenttask=str(-int(u.currenttask))
                    replacecache(uid,u)
                    return [-1,u.currenttask]
                u.currenttask=str(int(u.currenttask)+1)#level satisfy move to next level
                u.taskstring='0'
                replacecache(uid,u)
                return [taskbonus[ct+1][0],u.currenttask]
    def tasknew3(u):
        #u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus)-1 or int(u.currenttask)<=(-len(taskbonus)+1):
                u.currenttask=str(-int(u.currenttask))
                u.taskstring=''
                replacecache(u.userid,u)
                return [-1,u.currenttask]
            else:
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:
                    u.currenttask=str(-int(u.currenttask))
                    replacecache(u.userid,u)
                    return [-1,u.currenttask]
                u.currenttask=str(int(u.currenttask)+1)
                u.taskstring='0'
                replacecache(u.userid,u)
                return [taskbonus[ct+1][0],u.currenttask]
    @expose('json')
    def newtask(self,uid,taskid):
        print "new task id"
        u=checkopdata(uid)
        u.currenttask=taskid#差taskstring
        return dict(id=1)  
    def mktaskstr(lev,num):#内部函数，任务字符串
        if lev-3>=len(tasklist)or num>=len(tasklist[lev-3]):
            return ''
        taskstring=tasklist[lev-3][num][0]+';'+str(tasklist[lev-3][num][3])+';'+str(tasklist[lev-3][num][4])
        i=5
        k=len(tasklist[lev-3][num])
        while i<k:
            taskstring=taskstring+';'+tasklist[lev-3][num][i]
            i=i+1
        return taskstring
    ###########################
    @expose(content_type="image/png")
    def returnfile(self,name):#客户端下载请求函数，图片名称不能含有‘.'字符，返回图片名称为输入参数name值
        try:
            openfile=open(name,'r')
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename=name'
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
        except:
            openfile=open('a','r')#如果没有查到图片，返回图片'a'
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
    @expose(content_type="text/plain")
    def updatescript(self,name):
        try:
            name1='script/'+name
            openfile=open(name1,'r')
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
        except:
            openfile=open('a','r')#如果没有查到图片，返回图片'a'
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
            
    #cache related 与缓存相关测试函数
    @expose('json')
    def gameexit(self,uid):
        cachewriteback(uid)
        deletecache(uid)
    @expose('json')
    def deletecache(self,uid):
        q=logging.getLogger('stchong')
        q.info('delete')
        deleteopdata(uid)
    @expose('json')
    def testwriteback(self,uid):
        ucache=mc.get(str(uid))
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um=copy.deepcopy(uc)
            return dict(id=uc.invitestring,u=um.invitestring)
        else:
            return dict(id=0)
    @expose('json')
    def testcache(self,uid):
        u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        addcache(uid,u)
    @expose('json')
    def getcache(self,uid):
        uc=mc.get(str(uid))
        if uc!=None:
            return dict(id=uc[0].userid,call=uc[1])
        else:
            return dict(id=0)
    @expose('json')
    def testwritecache(self,uid):
        u=checkopdata(uid)#cache
        u.invitestring='testcache'
        replacecache(uid,u)#重要
        
        return dict(string=u.invitestring)
    @expose('json')
    def writeback(self,uid):
        ucache=mc.get(str(uid))
        
        
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um.userid=uc.userid
            um.labor_num=uc.labor_num
            um.population=uc.population
            um.exp=uc.exp
            um.corn=uc.corn
            um.cae=uc.cae
            um.nobility=uc.nobility
            um.subno=uc.subno
            um.infantry1_num=uc.infantry1_num
            um.cavalry1_num=uc.cavalry1_num
            um.scout1_num=uc.scout1_num
            um.person_god=uc.person_god
            um.person_god_lev=uc.person_god_lev
            um.wealth_god=uc.wealth_god
            um.wealth_god_lev=uc.wealth_god_lev
            um.food_god=uc.food_god
            um.food_god_lev=uc.food_god_lev
            um.war_god=uc.war_god
            um.war_god_lev=uc.war_god_lev
            um.user_kind=uc.user_kind
            um.otherid=uc.otherid
            um.lev=uc.lev
            um.empirename=uc.empirename
            um.food=uc.food
            um.populationupbound=uc.populationupbound
            um.wood=uc.wood
            um.stone=uc.stone
            um.specialgoods=uc.specialgoods
            um.treasurebox=uc.treasurebox
            um.treasurenum=uc.treasurenum
            um.landkind=uc.landkind
            um.visitnum=uc.visitnum
            um.allyupbound=uc.allyupbound
            um.allynum=uc.allynum
            um.infantry2_num=uc.infantry2_num
            um.cavalry2_num=uc.cavalry2_num
            um.scout3_num=uc.scout3_num
            um.scout2_num=uc.scout2_num
            um.infantry3_num=uc.infantry3_num
            um.cavalry3_num=uc.cavalry3_num
            um.loginnum=uc.loginnum
            um.minusstate=uc.minusstate
            um.monsterlist=uc.monsterlist
            um.monsterdefeat=uc.monsterdefeat
            um.rate=uc.rate
            um.allycancel=uc.allycancel
            um.defencepower=uc.defencepower
            um.battleresult=uc.battleresult
            um.nbattleresult=uc.nbattleresult
            um.wealthgodtime=uc.wealthgodtime
            um.foodgodtime=uc.foodgodtime
            um.wargodtime=uc.wargodtime
            um.popgodtime=uc.popgodtime
            um.newcomer=uc.newcomer
            um.castlelev=uc.castlelev
            um.infantrypower=uc.infantrypower
            um.cavalrypower=uc.cavalrypower
            um.currenttask=uc.currenttask
            um.taskstring=uc.taskstring
            um.tasknum=uc.tasknum
            um.invitestring=uc.invitestring
            um.signtime=uc.signtime
            um.tid=uc.tid
            um.paytime=uc.paytime
            um.hid=uc.hid
            um.monstertime=uc.monstertime
            um.invite=uc.invite
            um.invited=uc.invited
            um.inviteid=uc.inviteid
            um.monster=uc.monster
            um.monlost=uc.monlost
            um.monfood=uc.monfood
            um.monpower=uc.monpower
            return dict(id=1)
        else:
            return dict(id=0)
    def addcache(uid,u):
        uli=[u,0]
        mc.add(str(uid),uli)
    def checkopdata(uid):
        try:
            u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            return u
        except:
            return None       
    def checkopdata2(uid):
        ul=mc.get(str(uid))
        #if ul!=None and ul[1]>=CACHEOP:
        #    cachewriteback(uid)#将cache中内容写回数据库
        #    deleteopdata(uid)#删除cache中对应对象
        #    u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        #    uli=[u,0]
        #    mc.add(str(uid),uli)
        #    return uli[0]            
        if ul==None:
            u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            uli=[u,0]
            mc.add(str(uid),uli)
            return uli[0]
        ul[1]=ul[1]+1
        mc.replace(str(uid),ul)
        return ul[0]
    def replacecache(uid,u):#将新值写入cache，与checkopdata成对使用
        return 1
        #ul=mc.get(str(uid))
        #if ul!=None:
        #    ul[0]=u
        #    mc.replace(str(uid),ul)
        #    cachewriteback(uid)
        #    return 1
        #else:
        #    return 0
    def deleteopdata(uid):
        return mc.delete(str(uid),time=0) 
    def cachewriteback(uid):
        ucache=mc.get(str(uid))        
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um.userid=uc.userid
            um.labor_num=uc.labor_num
            um.population=uc.population
            um.exp=uc.exp
            um.corn=uc.corn
            um.cae=uc.cae
            um.nobility=uc.nobility
            um.subno=uc.subno
            um.infantry1_num=uc.infantry1_num
            um.cavalry1_num=uc.cavalry1_num
            um.scout1_num=uc.scout1_num
            um.person_god=uc.person_god
            um.person_god_lev=uc.person_god_lev
            um.wealth_god=uc.wealth_god
            um.wealth_god_lev=uc.wealth_god_lev
            um.food_god=uc.food_god
            um.food_god_lev=uc.food_god_lev
            um.war_god=uc.war_god
            um.war_god_lev=uc.war_god_lev
            um.user_kind=uc.user_kind
            um.otherid=uc.otherid
            um.lev=uc.lev
            um.empirename=uc.empirename
            um.food=uc.food
            um.populationupbound=uc.populationupbound
            um.wood=uc.wood
            um.stone=uc.stone
            um.specialgoods=uc.specialgoods
            um.treasurebox=uc.treasurebox
            um.treasurenum=uc.treasurenum
            um.landkind=uc.landkind
            um.visitnum=uc.visitnum
            um.allyupbound=uc.allyupbound
            um.allynum=uc.allynum
            um.infantry2_num=uc.infantry2_num
            um.cavalry2_num=uc.cavalry2_num
            um.scout3_num=uc.scout3_num
            um.scout2_num=uc.scout2_num
            um.infantry3_num=uc.infantry3_num
            um.cavalry3_num=uc.cavalry3_num
            um.loginnum=uc.loginnum
            um.minusstate=uc.minusstate
            um.monsterlist=uc.monsterlist
            um.monsterdefeat=uc.monsterdefeat
            um.rate=uc.rate
            um.allycancel=uc.allycancel
            um.defencepower=uc.defencepower
            um.battleresult=uc.battleresult
            um.nbattleresult=uc.nbattleresult
            um.wealthgodtime=uc.wealthgodtime
            um.foodgodtime=uc.foodgodtime
            um.wargodtime=uc.wargodtime
            um.popgodtime=uc.popgodtime
            um.newcomer=uc.newcomer
            um.castlelev=uc.castlelev
            um.infantrypower=uc.infantrypower
            um.cavalrypower=uc.cavalrypower
            um.currenttask=uc.currenttask
            um.taskstring=uc.taskstring
            um.tasknum=uc.tasknum
            um.invitestring=uc.invitestring
            um.paytime=uc.paytime
            um.tid=uc.tid
            um.hid=uc.hid
            um.monstertime=uc.monstertime
            um.invite=uc.invite
            uc.invited=uc.invited
            um.inviteid=uc.inviteid
            um.monster=uc.monster
            um.monlost=uc.monlost
            um.monfood=uc.monfood
            um.monpower=uc.monpower
            return 1
        else:
            return 0
    @expose('json')
    def memm(self):
        mc.add('a','b')
        value=mc.get('a')
        return dict(id=value)           
    #cache related
    
    @expose('json')#打分函数，在用户达到5级时调用，若用户没有评分，则在用户10级时再次调用，奖励5cae
    def rate(self,uid):
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.rate=1
        u.cae=u.cae+5
        print inspect.stack()[0]
        return dict(id=1)
    @expose('json')
    def levup(self,uid,lev):#operationalData:update,modify 用户升级时调用，uid为用户userid，lev为目标等级，10，30,60,100级时增加人口上限
        u=checkopdata(uid)#cache
        u.corn=u.corn+(int(lev))*200#奖励corn 用户等级*20 
        u.lev=int(lev)
        tasklist=[]
        task=[-1,-1]
        if u.lev%10==0:
            u.populationupbound=u.populationupbound+500
            u.cae=u.cae+u.lev/10
            print inspect.stack()[0]
        if u.currenttask!='-1' and int(u.currenttask)<0:
            task=tasknew3(u)
            #u.currenttask=task[0]
            u.taskstring='0'
        replacecache(uid,u)#cache
        task1=task[0]
        if task[0]<0:
            task1=-1
        xs=[]
        xs=DBSession.query(Papayafriend).filter_by(papayaid=u.otherid).filter_by(user_kind=u.user_kind).all()
        for xxs in xs:
            xxs.lev=u.lev
        if u.lev==10 and u.rate==0:#当用户到达10级且没有评分，则返回rate=0告知客户端。
            return dict(task=task1,tasklist=tasklist,rate=0,id=1)
        return dict(task=task1,id=1,tasklist=tasklist)        
    def timejudge(t):#判断当前时间和传入时间t相隔时间是否超过1天。在selectgift函数中被调用
        t2=int(time.mktime(time.localtime())-time.mktime(beginTime))
        s=t2/86400-t/86400
        if s<1 :#如果没有超过一天，返回false
            return False
        else:
            return True
    def loginBonus(u):#called when login;u is the user;operationalData:query->update 用户u的每日登录奖励
            time1=int(time.mktime(time.localtime())-time.mktime(beginTime))
            ds=DBSession.query(Datesurprise).filter_by(uid=u.userid).one()
            s=time1/86400-u.logintime/86400
            card=None
            try:
                card=DBSession.query(Card).filter_by(uid=u.userid).one()
            except:
                nc=Card(uid=u.userid)
                DBSession.add(nc)
                c1=DBSession.query('LAST_INSERT_ID()')
                nuid=c1[0]
                card=DBSession.query(Card).filter_by(uid=u.userid).one()
            
            if u.newcomer<3:#当处在新手任务时，不给登录奖励
                return 0
            if s>1:#重新计算登录奖励
                u.loginnum=0
                u.logincard=0
            if ds.datesurprise==0 :
                
                bonus=loginbonuslist[u.loginnum]#根据连续登录次数决定登录奖励
                if bonus>0 :
                    u.corn=u.corn+bonus
                else:
                    u.cae=u.cae-bonus
                    print inspect.stack()[0]
                if u.loginnum<4:
                    u.loginnum=u.loginnum+1
                else:
                    u.loginnum=0
                                
                u.logincard=u.logincard+1

                if u.logincard>=u.loginmax:
                    u.loginmax=u.loginmax+1
                    if card!=None:
                        card.logincard=u.loginmax
                ds.datesurprise=1
                return bonus
            else:
                return 0 
    def inornot(num,li):#辅助函数，判断整数num是否在整数列表li中 in or not
        if len(li)==0:
            return False
        for i in li:
            if num==i :
                return True
        return False
    def present(u):#没有被使用，返回4中随机建筑
        index=random.randint(0,len(randombuilding)-1)
        i=0
        li=[]
        while i<4 :
            while randombuilding[index][1]>u.lev or inornot(index,li)==True:
                index=random.randint(0,len(randombuilding)-1)
            i=i+1
            li.append(randombuilding[index][0])
            index=random.randint(0,len(randombuilding)-1)
        return li

    def getbonus(u):#计算打败怪兽后的奖励，返回特殊物品字符串，在对外接口defeatmonster中被调用
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        k=0
        if nobility>=0 and nobility<=1:
            k=1
        elif nobility>=2 and nobility<=4:
            k=2
        else:
            k=3
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        strr=u.specialgoods.split(';')
        for x in strr:#添加特殊物品
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    y1=y1+1
                    break
                j=j+1
            j=0
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:#拼接string
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s        
        return s
    def getbonusbattle(u,k):#战斗胜利后的奖励，在warresult中被调用 type=1,got type=0,lost
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    #if type==1:#got
                    y1=y1+1
                    #else:#lost
                    #    y1=y1-1
                    #    if y1<0:
                    #        y1=0
                    break
                j=j+1
            j=0
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        i=0
        s=''
        for x in num2:
            if i==0:
                s=s+str(x)
                i=1
            else:
                s=s+'!'+str(x)
        
        return s      
    #def getbonusbattle2(u,k,type):#type=1,got,type=0,lost,k=0进攻胜利，1，进攻失败，2防御胜利，3防御失败
              
    def getbonusbattle3(u,k,type):#战斗胜利后的奖励，在warresult中被调用 type=1,got type=0,lost
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    if type==1:#got
                        y1=y1+1
                    else:#lost
                        y1=y1-1
                        if y1<0:
                            y1=0
                    break
                j=j+1
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        i=0
        s=''
        for x in num2:
            if i==0:
                s=s+str(x)
                i=1
            else:
                s=s+'!'+str(x)
        return s

    def returnSoldier(u):#不再使用，返回用户u各种士兵列表
        soldier=[]
        soldier.append(u.infantry1_num)
        soldier.append(u.infantry2_num)
        soldier.append(u.infantry3_num)
        soldier.append(u.cavalry1_num)
        soldier.append(u.cavalry2_num)
        soldier.append(u.cavalry3_num)
        return soldier
    def returnsentouryoku(u):#返回用户u总战斗力
        sentouryoku=[]
        power=u.infantrypower+u.cavalrypower
        return power     
    ##################怪兽相关    
    @expose('json')
    def monsterrefresh(self,userid,monsterstr):#对外接口，客户端刷新怪兽字符串，monsterstr
        #u=DBSession.query(operationalData).filter_by(userid=int(userid)).one()
        midlist=[]
        u=checkopdata(userid)#cache
        u.monsterlist=monsterstr
        #u.monsterdefeat=0
        u.monstertime=0
        if monsterstr=='' or monsterstr==None:
            return dict(id=0)
        monsterlist=monsterstr.split(';')
        for monster in monsterlist:
            mm=monster.split(',')
            midlist.append(int(mm[0]))
        i=0
        #max=midlist[0]
        #while i<len(midlist):
        #    if max<midlist[i]:
        #        max=midlist[i]
        #    i=i+1
        u.monster=u.monster+1 
        replacecache(userid,u)#cache
        
        return dict(id=1) 
    @expose('json')
    def delaymonster(self,uid):
        u=checkopdata(uid)#cache
        cf=0
        if u.monster<=10:
            cf=1
        elif u.monster<=20:
            cf=2
        elif u.monster<=30:
            cf=3
        elif u.monster<=41:
            cf=4
        else:
            cf=5
        if u.cae-cf<0:
            return dict(id=0)
        u.cae=u.cae-cf
        print inspect.stack()[0]
        u.monstertime=u.monstertime+86400
        return dict(id=1)
    @expose('json')
    def speedupmonster(self,uid,monsterstr): 
        
        u=checkopdata(uid)#cache
        cf=0
        if u.monster<=10:
            cf=1
        elif u.monster<=20:
            cf=2
        elif u.monster<=30:
            cf=3
        elif u.monster<=41:
            cf=4
        else:
            cf=5
        if u.cae-cf<0:
            return dict(id=0)
        u.cae=u.cae-cf
        print inspect.stack()[0]
        u.monsterlist=monsterstr
        u.monstertime=0
        u.monster=u.monster+1
        return dict(id=1)     
    @expose('json')   
    def monstercomplete(self,uid):
        u=checkopdata(uid)
        refreshtime=random.randint(12,24)
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        u.monstertime=t+refreshtime*3600
        u.monsterlist=''
        if u.lev<=8:
            u.exp=u.exp+(int(u.monpower+4-1)/4)
        elif u.lev<=14:
            u.exp=u.exp+int((2*u.monpower+5-1)/5)
        else:
            u.exp=u.exp+int((u.monpower+2-1)/2)
        u.corn=u.corn+u.monlost*30
        u.monlost=0
        return dict(monstertime=u.monstertime)
    @expose('json')
    def foodlost(self,uid):
        print "foodlost " + str(uid)
        try:
            user=checkopdata(uid)
            foodlost=0
            ds=None
            try:
                ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()   
            except:
                return dict(foodlost=0)
            if ds.monfood==0 or ds.monfood==None :
                ds.monfood = 1
            elif ds.monfood < 2:
                ds.monfood += 1
            elif ds.monfood == 2:
                ds.monfood += 1
                monlist = user.monsterlist
                monlist = monlist.split(';')
                length = len(monlist)
                if length > 0:
                    res = monlist[0].split(',')
                    if len(res) < 2:
                        return dict(foodlost = 0)
                foodlost = (0.03 + length*1.0/200) * user.food
                foodlost = int(foodlost)
                user.food -= foodlost
                #user.monfood=1
                print "lostfood " + str(foodlost)
                return dict(foodlost=foodlost)
        except :
            return dict(foodlost=0)
        return dict(foodlost = 0)
    @expose('json')
    def defeatmonster(self,uid,gridid):#对外接口，与怪兽进行战斗
        listsoldier=[]
        l2=[]
        mlist=[]
        mmlist=[]
        monsterid=-1
        mstr=''
        nobility=0
        yuzhi=3#随机值
        powerlost=0
        i=0
        s=''
        muu=0
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            monsterstr=u.monsterlist
            nobility=u.nobility
            if monsterstr=='' or monsterstr==None:
                return dict(id=0)
            mlist=monsterstr.split(';')
            for m in mlist:                
                ml=m.split(',')
                if len(ml)<2:
                    continue
                if gridid==ml[1]:
                    monsterid=int(ml[0])
                    break
            if monsterid==-1:
                return dict(id=0)
            listsoldier=returnSoldier(u)
            up=returnsentouryoku(u)#user power to defeat monster
            k=monsterlist[monsterid]
            if u.monster>=60:
                k=k+u.monster-60+1
            #k=monsterlist[monsterid/3]
            #if monsterid%3==1:
            #    k=int(k*1.5)
            #elif monsterid%3==2:
            #    k=int(k*2)
            if up-k<0:
                return dict(id=30)
            else:
                #k1=k+5
                #k2=k-5
                #k=random.randint(k2,k1)
                #muu=int(k/2)
                
                #mu=random.randint(muu-3,muu+3)
                if u.lev<=8:
                    mu=int((k+2-1)/2)
                    u.exp=u.exp+(int(k+4-1)/4)
                elif u.lev>8 and u.lev<=14:
                    mu=int((3*k+5-1)/5)
                    u.exp=u.exp+int((2*k+5-1)/5)
                else:
                    mu=int((65*k+100-1)/100)
                    u.exp=u.exp+int((k+2-1)/2)
                powerlost=mu
                
                #u.exp=u.exp+int(mu/2)
                u.corn=u.corn+mu*30
                if monsterid%3==0:
                    t=1
                elif monsterid%3==1:
                    t=2
                else:
                    t=3
                s=getbonusbattle(u,t)
                mu=u.infantrypower-mu
                if mu>=0:
                    u.infantrypower=mu
                else:
                    u.infantrypower=0
                    u.cavalrypower=u.cavalrypower+mu
            i=0
            for m in mlist:
                ml=m.split(',')
                if ml[1]!=gridid:
                    if i==0:
                        mstr=mstr+m
                        i=1
                    else:
                        mstr=mstr+';'+m
            u.monsterlist=mstr
            #u.monsterdefeat=u.monsterdefeat+1
            card=0
            u.monlost=powerlost
            u.monpower=k
            ##计算荣誉
            count=u.monsterdefeat.split(';')
            ct=[]
            if count!=None and len(count)>0:
                for c in count:
                    ct.append(int(c))
                if monsterid!=-1:
                    ct[int(monsterid/3)]=ct[int(monsterid/3)]+1
                if ct[int(monsterid/3)]==10:
                    card=1
                elif ct[int(monsterid/3)]==25:
                    card=2
                elif ct[int(monsterid/3)]==50:
                    card=3
                elif ct[int(monsterid/3)]==100:
                    card=4
                elif ct[int(monsterid/3)]==500:
                    card=5
                i=0
                ss=''
                for cc in ct:
                    if i==0:
                        ss=ss+str(cc)
                        i=1
                    else:
                        ss=ss+';'+str(cc)
                u.monsterdefeat=ss
             ##计算荣誉
            #u.monsterdefeat=ss       
            replacecache(uid,u)#cache
            return dict(id=1,cardid=card,powerlost=powerlost,infantrypower=u.infantrypower,cavalrypower=u.cavalrypower,specialgoods=s)  
        except InvalidRequestError:
            return dict(id=0)
    ##################
    ##################负面状态相关
    def checkminusstate(gridid,mstr):#str为表示负面状态的字符串，函数用于检查此城市的负面状态中是否含有str状态，在对外接口addminusstate中使用
        mlist=mstr.split(mstr)
        i=0
        s=''
        for m in mlist:
            if u.minusstate.find(m)!=-1:
                if i==0:
                    s=m
                    i=1
                else:
                    s=s+';'+m
        return s   
    def checkminusstate2(u,str):#str为表示负面状态的字符串，函数用于检查此城市的负面状态中是否含有str状态，在对外接口addminusstate中使用
        if u.minusstate.find(str)!=-1:
            return True
        else:
            return False
    @expose('json')
    def addminusstate(self,city_id,minusstr):#对外接口，在城市city_id的grid_id处，增加类型为type的异常状态，异常状态字符串在warmap数据库中
        #t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
        str2=minusstr
        strminus=minusstr#异常状态字符串，最后加', '是为了使用checkminusstate的方便
        strminus=checkminusstate(war,minusstr)
        str3=''
        x=[]
        minus=[] 
        x=minusstr.split(';')
        minus=war.minusstate.split(';')
        if minus==None or len(minus)==0:
            minus=[]
            minus.append(war.minusstate)
        if x==None or len(x)==0:
            x=[]
            x.append(minusstr)
        xy=[]
        mark=0
        for xx in x:
            xm=xx.split(',')
            for mm in minus:
                mmx=mm.split(',')
                if mmx[1]==xx[1]:
                    mark=1
            if mark==0:
                xy.append(xx)
            mark=0
        i=0
        for xyy in xy:
            if i==0:
                str3=str3+xyy[0]+','+xyy[1]
                i=1
            else:
                str3=str3+';'+xyy[0]+','+xyy[1]
                         
        if war.minusstate=='':
            war.minusstate=str3
            return dict(id=1)
        else:
            if strminus!='':
                war.minusstate=war.minusstate+';'+str3
                return dict(id=1)    
            else:
                return dict(id=0)
    @expose('json')
    def addminusstate2(self,city_id,type,grid_id):#对外接口，在城市city_id的grid_id处，增加类型为type的异常状态，异常状态字符串在warmap数据库中
        #t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
        str2=type+','+grid_id+', '
        strminus=type+','+grid_id#异常状态字符串，最后加', '是为了使用checkminusstate的方便  
        mlist=[]  
        if war.minusstate=='':
            war.minusstate=strminus
            return dict(id=1)
        else:
            mlist=war.minusstate.split(';')
            if len(mlist)==0:
                x=war.minusstate.split(',')
                if len(x)>1 and x[1]==grid_id:
                    return dict(id=0)
            else:
                for m in mlist:
                    xx=m.split(',')
                    if len(xx)>1:
                        if xx[1]==grid_id:
                            return dict(id=0)
            war.minusstate=war.minusstate+';'+strminus
            return dict(id=1)            
    @expose('json')
    def eliminusstate(self,uid,city_id,grid_id):#对外接口，用户uid对城市city_id grid_id处的负面状态进行消除操作
        stri=''
        i=0
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        minuslist=[]
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            strminus=war.minusstate
            minuslist=strminus.split(';')
            if strminus=='' or strminus==None or minuslist==None or len(minuslist)==0:
                return dict(id=0)
            else:
                if len(minuslist)==0:
                    minuslist.append(strminus)
                i=0
                for ml in minuslist :
                    if ml=='' or ml==None:
                        continue
                    mle=ml.split(',')
                    if len(mle)>=2:
                        if mle[1]==grid_id :
                            if mle[0]=='3':
                                return dict(id=0)
                            mle[0]='3'
                        if i==0:
                            stri=stri+mle[0]+','+mle[1]
                            i=1
                        else:
                            stri=stri+';'+mle[0]+','+mle[1]
                war.minusstate=stri
                lev=int((u.lev-1)/10)
                u.corn=u.corn+50+lev*20
                u.exp=u.exp+1+lev*1
                #u.corn=u.corn+50
                if u.userid!=war.userid:#当不是打理自己的城堡时，记录新闻
                    try:
                        n=DBSession.query(News).filter_by(uid=war.userid).filter_by(fpapayaid=u.otherid).filter_by(fuser_kind=u.user_kind).filter_by(kind=1).one()
                        n.time=t
                    except:
                        addnews(war.userid,u.otherid,1,t,u.user_kind) 
                replacecache(uid,u)  
                return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)         
    def minusstateeli(user,war,stri,t1):#自动消除负面状态，返回值mark，当mark=1时，只给经验。在harvest，finipop，production接口中使用
        mark=0
        if war.minusstate=='' or war.minusstate==None:
            return 0
        msl=war.minusstate.split(';')
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        ss=''
        sss=''
        day1=0
        i=0
        if msl==None:
            return 0
        for msle in msl :
            if msle=='' or msle==None:
                continue
            mslee=msle.split(',')
            if len(mslee)<2:
                continue
            day=t/86400-t1/86400
            if stri==mslee[1] and user.lev<10:

                if day>=3:
                    mark=1
                           
            elif stri==mslee[1] and user.lev>=10 and user.lev<20:
                if day>=5:
                    mark=1
                        
            elif stri==mslee[1]:
                if day>=7:
                    mark=1
            else:
                sss=sss+mslee[0]+','+mslee[1]+';'
                if i==0:
                    ss=ss+msle
                    i=1
                else:
                    ss=ss+';'+msle   
        war.minusstate=ss
        return mark
    ################
    ################结盟相关                       
    @expose('json')
    def makeally(self,uid,fid):#对外接口，用户uid向fid结盟
        uid=int(uid)
        fid=int(fid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        #f=DBSession.query(operationalData).filter_by(userid=fid).one()
        u=checkopdata(uid)#cache
        f=checkopdata(fid)#cache
        try:
            a1=DBSession.query(Ally).filter_by(uid=uid).filter_by(fid=fid).one()
            return dict(id=0)
        except InvalidRequestError:   
            if u.allynum < u.allyupbound:
                u.allynum=u.allynum+1
                newally=Ally(uid=uid,fid=fid)
                DBSession.add(newally)  
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0) 
                            
    @expose('json')
    def cancelally(self,uid,fid):#对外接口，用户uid取消与fid用户的结盟关系
        uid=int(uid)
        fid=int(fid)
        u=checkopdata(uid)#cache
        try:
            if u.cae-5<0:
                return dict(id=0)
            u.cae=u.cae-5
            print inspect.stack()[0]
            u.allynum=u.allynum-1
            if u.allynum<0:
                u.allynum=0
            a1=DBSession.query(Ally).filter_by(uid=uid).filter_by(fid=fid).one()            
            DBSession.delete(a1)      
            replacecache(uid,u)#cache  
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)                                  
    @expose('json')
    def addallyupbound(self,userid):#增加可结盟数上限
        try:
            userid=int(userid)
            #u=DBSession.query(operationalData).filter_by(userid=userid).one()
            u=checkopdata(userid)#cache
            if u.nobility>NOBILITYUP :
                return dict(id=0)
            sub=u.allyupbound-allyup[u.nobility]
            cae=5*(sub+1)+5
            if u.cae-cae>=0:
                u.cae=u.cae-cae
                u.allyupbound=u.allyupbound+1
                print inspect.stack()[0]
                return dict(id=1)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    ################
    ################宝箱相关
    @expose('json')
    def newtbox(self,user_id,num):#对外接口，用户user_id,生成新宝箱，num为宝箱座位数
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            u.treasurenum=int(num)
            u.treasurebox=''
            replacecache(user_id,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')#operationalData:query->update
    def helpopen(self,user_id,fuser_id):#对外接口，用户user_id帮助 用户fuser_id 打开宝箱
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        #u1=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
        #u2=DBSession.query(operationalData).filter_by(userid=int(fuser_id)).one()
        u1=checkopdata(user_id)#cache
        u2=checkopdata(fuser_id)#cache
        papayaid1=u1.otherid
        blist=[]
        if u2.treasurebox!='':
            s=(u2.treasurebox).split(';')
            length=len(s)
            if length<u2.treasurenum:
                u2.treasurebox=u2.treasurebox+';'+str(papayaid1)
                u1.corn=u1.corn+1000#user who helped his or her friend opening the treasurebox will get a 1000 corn bonus
                addnews(int(fuser_id),u1.otherid,5,t,u1.user_kind)
                replacecache(user_id,u1)#cache
                replacecache(fuser_id,u2)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        else:
            u2.treasurebox=str(papayaid1)
            u1.corn=u1.corn+1000#user who helped his or her friend opening the treasurebox will get a 1000 corn bonus
            addnews(int(fuser_id),u1.otherid,5,t,u1.user_kind)
            replacecache(user_id,u1)#cache
            replacecache(fuser_id,u2)#cache            
            return dict(id=1)
    @expose('json')
    def selfopen(self,user_id):#用户使用cae币打开宝箱
        u=checkopdata(user_id)#cache
        if u.cae-1>=0:
            if u.treasurebox!='':
                s=(u.treasurebox).split(';')
                length=len(s)
                if length<u.treasurenum:
                    u.treasurebox=u.treasurebox+';'+str(-1)
                    u.cae=u.cae-1
                    print inspect.stack()[0]
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                u.treasurebox='-1'
                u.cae=u.cae-1
                print inspect.stack()[0]
                return dict(id=1)
        else:
            return dict(id=0)
    @expose('json')
    def completeopen(self,user_id):#对外接口，完成打开宝箱，num为特殊物品列表
        #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
        try:
            u=checkopdata(user_id)#cache
            u.treasurenum=0
            u.treasurebox=''
            num=opentreasurebox(u)
            replacecache(user_id,u)#cache
            return dict(id=1,specialgoods=num)
        except:
            return dict(id=0)
    def opentreasurebox(u):#宝箱礼物 在对外接口completeopen中被调用，返回两种特殊物品
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        k=2
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        #a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                #num2.append(x1)
                if a1==x1:
                    y1=y1+1
                    #num2.append(y1)
                    break
                j=j+1
            j=0
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        cornbonus=2000+u.lev*50
        u.corn=u.corn+cornbonus
        u.exp=u.exp+5+u.lev
        return num2        
    ###############
        
    def specialgoods(ground_id,stri,u):#判断建筑物的特殊物品要求是否得到满足 return true if special goods enough;operationalData:query->update
        stri='111'
        stru=u.specialgoods
        num1=[]
        num2=[]
        if stru==None:
            return True
        struset=stru.split(';')
        if struset!=None:
            for su in struset:
                suset=su.split(',')
                
                type=suset[0]
                ac=suset[1]
                num1.append([type,ac])
            if ground_id>=100 and ground_id<=199:
                stri=housebuild[ground_id-100][6]
            elif ground_id>=200 and ground_id<=299:
                stri=milbuild[ground_id-200][7]
            elif ground_id>=300 and ground_id<=399:
                stri=businessbuild[ground_id-300][7]
            else:
                return True
            if stri=='111':
                return True
            else:
                if stri==None:
                    return True
                strset=stri.split(';')
                for ss in strset:
                    ssset=ss.split(',')
                    num2.append([ssset[0],ssset[1]])
                for x in num2:
                    for y in num1:
                        if y[0]==x[0]:
                            if int(y[1])-int(x[1])>=0:
                                y[1]=str(int(y[1])-int(x[1]))
                            else:
                                return False
                strre=''
                mark=0
                for y in num1:
                    tempstr=y[0]+','+y[1]
                    if mark==0:
                        strre=strre+tempstr
                        mark=1
                    else:
                        strre=strre+';'+tempstr
                u.specialgoods=strre
                return True
        else:
            return True
    def getGround_id(ground_id):# return lis[]
        castle=[[-1,-1]]
        error=[[-2,-2]]
        if ground_id==0:
            return None#castle
        elif ground_id>=1 and ground_id<=99:#resource
            return resourcebuild[ground_id-1]
        elif ground_id>=100 and ground_id<=199:#house
            return housebuild[ground_id-100]
        elif ground_id>=200 and ground_id<=299:#military
            return milbuild[ground_id-200]
        elif ground_id>=300 and ground_id<=399:#business
            return businessbuild[ground_id-300]
        elif ground_id>=400 and ground_id<420:#god
            return godbuild[ground_id-400]
        elif ground_id>=420 and ground_id<=424:
            return friendGod[ground_id-420]
        elif ground_id>=500 and ground_id<=599:#decoration
            return decorationbuild[ground_id-500]
        elif ground_id>=600 and ground_id<=699:
            return statuebuilding[ground_id-600]
        else:
            return None
    ###############赠送礼物相关        
    def sg(otherid,user_kind,sp):#赠送特殊物品作为礼物
        stri='111'        
        uu=DBSession.query(operationalData).filter_by(otherid=otherid).filter_by(user_kind=user_kind).one()#7.29 otherid改为varchar类型
        u=checkopdata(uu.userid)#cache
        stru=u.specialgoods
        num1=[]
        num2=[]
        sp1=alphabet[sp]
        if stru==None:
            return True
        struset=stru.split(';')
        if struset!=None:
            for su in struset:
                suset=su.split(',')
                
                type=suset[0]
                ac=suset[1]
                num1.append([type,ac])
            for y in num1:
                if y[0]==sp1:
                    y[1]=str(int(y[1])+1)
            strre=''
            mark=0
            for y in num1:
                tempstr=y[0]+','+y[1]
                if mark==0:
                    strre=strre+tempstr
                    mark=1
                else:
                    strre=strre+';'+tempstr
            u.specialgoods=strre
            replacecache(u.userid,u)#cache
            return strre
        else:
            return ''            
    @expose('json')
    def getgift(self,uid,off,num):#uid=papayaid
        uid=uid
        newslist=[]
        nl=[]
        #num=11
        x=0 
        off=int(off)
        num=int(num)   
        giftlist=[]    
        try:
            giftset=DBSession.query(Gift).filter_by(fid=uid).filter_by(received=0).order_by(Gift.id).all()
            for n in giftset:
                ntemp=[n.id,n.uid,n.present,n.askorgive]
                nl.append(ntemp)    
            if len(nl)==0 or nl==None :
                return dict(gift=[])
            i=off
            l1=num+off
            if l1>len(nl):
                l1=len(nl)
            while i<l1:
                n1=[nl[i][0],nl[i][1],nl[i][2],nl[i][3]]
                i=i+1
                newslist.append(n1)
            k=len(newslist)-1
            while k>=0:
                giftlist.append(newslist[k])
                k=k-1    
            #return dict(id=1)
            return dict(gift=giftlist)
                
        except InvalidRequestError:
            return dict(gift=[])               
    @expose('json')
    def selectgift(self,uid,fid,specialgoods,askorgive):#对外接口，选择一种特殊物品作为礼物，0：赠送，1索要 operationalData:query;Gift:insert->update
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        fid=int(fid)
        #f=DBSession.query(operationalData).filter_by(userid=fid).one()
        f=checkopdata(fid)
        upapayaid=u.otherid
        fpapayaid=f.otherid
        specialgoods=int(specialgoods)
        askorgive=int(askorgive)
        ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
        try:
            n=DBSession.query(Gift).filter_by(uid=u.otherid).filter_by(fid=f.otherid).filter_by(askorgive=askorgive).all()
            for nn in n:
                if ti/86400-nn.time/86400<1:
                    return dict(id=0)
        except:
            xx=0
        ng=Gift(uid=upapayaid,fid=fpapayaid,askorgive=askorgive,present=specialgoods,fkind=f.user_kind,ukind=u.user_kind)
        DBSession.add(ng)
        c1=DBSession.query('LAST_INSERT_ID()')
        id=c1[0][0]
        if askorgive==0:#2011.7.13 addnews
            addnews(fid,u.otherid,2,int(time.mktime(time.localtime())-time.mktime(beginTime)),u.user_kind)        
        
        
        try:
            sgift=DBSession.query(Gift).filter_by(id=id).one()
            sgift.time=ti
            #c1.time=
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
        """
        try:
            sgift=DBSession.query(Gift).filter_by(uid=upapayaid).filter_by(fid=fpapayaid).filter_by(ukind=u.user_kind).filter_by(fkind=f.user_kind).filter_by(askorgive=askorgive).one()
            #tt=sgift.time
            #return dict(id=timejudge(sgift.time))
            if timejudge(sgift.time)==True:
                
                t1=sgift.time
                sgift.time=int(time.mktime(time.localtime())-time.mktime(beginTime))
                sgift.present=specialgoods
                if askorgive==0:#2011.7.13 addnews
                    addnews(fid,u.otherid,2,sgift.time,u.user_kind)
                sgift.received=0
                return dict(id=1)
            else:
                #x=int(time.mktime(time.localtime())-time.mktime(beginTime))/86400-tt/86400
                return dict(id=0)
        except InvalidRequestError:
            ng=Gift(uid=upapayaid,fid=fpapayaid,askorgive=askorgive,present=specialgoods,fkind=f.user_kind,ukind=u.user_kind)
            DBSession.add(ng)
            c1=DBSession.query('LAST_INSERT_ID()')
            sgift=DBSession.query(Gift).filter_by(uid=upapayaid).filter_by(fid=fpapayaid).filter_by(askorgive=askorgive).one()
            sgift.time=int(time.mktime(time.localtime())-time.mktime(beginTime))
            if askorgive==0:#2011.7.13 addnews
                addnews(fid,u.otherid,2,sgift.time,u.user_kind)            
            return dict(id=1)
        """
    def giftstring(uid):#从gift数据表中查到用户uid相关的礼物信息logsign中使用...fid,present,askorgive;Gift:query
        #uid=int(uid)
        s=''
        mark=0
        try:
            sgift=DBSession.query(Gift).filter_by(fid=uid)
            if sgift!=None:
                for sg in sgift:
                    if sg.received==0 :
                        if mark==0:
                            s=s+str(sg.uid)+','+str(sg.present)+','+str(sg.askorgive)
                            sg.received=1
                            mark=1
                        else:
                            s=s+';'+str(sg.uid)+','+str(sg.present)+','+str(sg.askorgive)
                            sg.received=1
            return s
        except InvalidRequestError:
            return '' 
    
    def completereceive(sg,gii):#Gift:update
        #for sg in sgift :
        if sg.uid==gii[0] and sg.present==int(gii[1]) and sg.askorgive==int(gii[2]) and sg.received==0:
            sg.received=1
            return 1
        return sg.uid
    #@expose('json')
    #def getgift(self,uid):
        
    @expose('json')
    def receivegift(self,uid,giftstr):#对外接口，接受礼物giftstr
        three=[]
        uid=int(uid)
        mark=0
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        sgift=DBSession.query(Gift).filter_by(fid=u.otherid).all()
        s1=[]
        if giftstr!='' and giftstr!=None:
            gifts=giftstr.split(';')
            for gi in gifts :
                gii=gi.split(',')
                three.append(gii)
            for gii in three:
                for ss in sgift:
                    if int(gii[2])==0:
                        if int(gii[1])>=0 and int(gii[1])<12:
                            if int(gii[3])==ss.id and gii[0]==ss.uid and int(gii[1])==ss.present and ss.askorgive==int(gii[2]) and ss.received==0:
                                specialg=int(gii[1])
                                s1.append(sg(u.otherid,u.user_kind,specialg))
                                ss.received=1
                            elif int(gii[3])==ss.id and int(gii[2])==2:
                                ss.received=1
                            
                    elif int(gii[2])==1:
                        fid=int(gii[0])
                        if int(gii[1])>=0 and int(gii[1])<12 :
                            #c=completereceive(ss,gii)
                            #if c==1:
                            if int(gii[3])==ss.id and gii[0]==ss.uid and int(gii[1])==ss.present and ss.askorgive==int(gii[2]) and ss.received==0:
                                specialg=int(gii[1])
                                s1.append(sg(fid,u.user_kind,specialg))
                                ss.received=1
                            elif int(gii[3])==ss.id and int(gii[2])==2:
                                ss.received=1       
                    else:
                        if int(gii[3])==ss.id:
                            ss.received=1    
                            fid=int(gii[0])                                             
                            #specialg=int(gii[1])
                                #s1.append(sg(fid,u.user_kind,specialg))
                            #else:
                            #    mark=c
                            #    continue
            
            #for ss in sgift:
            #    for gii in three:
            #        if int(gii[2])==0 :
             #           if int(gii[1])>=0 and int(gii[1])<12 :                        
             #               #c=completereceive(ss,gii)
             #               if gii[0]==ss.uid and int(gii[1])==ss.present and ss.askorgive==int(gii[2]):
                                #return dict(id=111)
             #                   specialg=int(gii[1])
             #                   s1.append(sg(u.otherid,u.user_kind,specialg))
                                
                            #else:
                            #    mark=c
                                
                            #    continue
               #     else:
                #        fid=int(gii[0])
               #         if int(gii[1])>=0 and int(gii[1])<12 :
               #             #c=completereceive(ss,gii)
                            #if c==1:
               #             if gii[0]==ss.uid and int(gii[1])==ss.present and ss.askorgive==int(gii[2]):
                #                specialg=int(gii[1])                            
                            #specialg=int(gii[1])
               #                 s1.append(sg(fid,u.user_kind,specialg))
                            #else:
                            #    mark=c
                            #    continue
            replacecache(uid,u)
            return dict(id=1,mark=mark)
        else:
            return dict(id=0)  
    #################
    #################访问好友                  
    @expose('json')
    def getfriend(self,userid,otherid,user_kind):#对外接口，用户userid 访问由otherid+user_kind确定的好友 get friends page;operationalData:query->updatewarMap:query;businessRead:query;visitFriend:query->update
        print "visit friend " + str(userid) + ' ' + str(otherid)
        userid=int(userid)
        friendid=-1
        u=None
        uu=None
        readstr=''
        lis=[]
        lis2=[]
        i=1
        city_id=0
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        city=None
        uw=None
        dv=None
        cardlist=[]
        visit=None
        bonus=0
        try:
            dv=DBSession.query(Datevisit).filter_by(uid=int(userid)).one()
            uu=checkopdata(userid)#cache
            u=DBSession.query(operationalData).filter_by(otherid=otherid).filter_by(user_kind=int(user_kind)).one()#7.29,otherid 
            uw=DBSession.query(warMap).filter_by(userid=u.userid).one()
            friendid=u.userid

            #city=DBSession.query(warMap).filter_by(userid=u.userid).one()
            if uw.city_id == 2763:#caesars building
                readstr = DBSession.query(businessRead).filter_by(city_id = uw.city_id).one()
                readstr = readstr.layout
            else:
                readstr = getCity(uw.city_id)

            visit=DBSession.query(Papayafriend).filter_by(uid=userid).filter_by(papayaid=otherid).one()
            try:
                ca=DBSession.query(Card).filter_by(uid=u.userid).one()
                cardlist.append(ca.logincard)
                cardlist.append(ca.foodcard)
                cardlist.append(ca.fortunecard)
                cardlist.append(ca.popcard)
                cardlist.append(ca.warcard)
                cardlist.append(ca.friendcard)
            except:
                cardlist=[]
            if visit.visited==0:#not visited
                print "not visited yet"
                bonus=100+5*(dv.visitnum)
                print "bonus " + str(bonus)
                mycity = DBSession.query(warMap).filter_by(userid = userid).one()
                buildings = DBSession.query(businessWrite).filter("city_id=:cid and ground_id >= 420 and ground_id <= 424 and finish = 1").params(cid=mycity.city_id).all() 
                print "friend god " + str(len(buildings))
                workTime = [3600, 21600, 86400]
                #only one friend god
                if len(buildings) > 0:
                    b = buildings[0];
                    if b.object_id >=0 and b.object_id < len(workTime) and workTime[b.object_id] > (t-b.producttime):
                        lev = b.ground_id-420;
                        bonus += friGodReward[lev]
                        print "friend God help"
                    else:
                        b.object_id = -1
                        b.producttime = 0
                
                print "bonus " + str(bonus)
                #增加访问奖励
                uu.corn=uu.corn+bonus#bonus
                dv.visitnum=dv.visitnum+1
                uu.visitnum=dv.visitnum
                
                visit.visited=1
                i=0
            viNews = DBSession.query(News).filter_by(uid=u.userid).filter_by(fpapayaid=uu.otherid).filter_by(kind=0).all()
            if len(viNews) == 0:
                addnews(u.userid,uu.otherid,0,t,uu.user_kind)#2011.7.13:add news
            else:
                news = viNews[0]
                news.time = t
            sub=0
            try:
                vf=DBSession.query(Victories).filter_by(uid=u.userid).one()
                sub=recalev(u,vf)
            except:
                sub=0
                
            
            return dict(loginNum = u.logincard, money = u.corn, id=otherid, sub=sub,cardlist=cardlist,monsterdefeat=u.monsterdefeat,hid=u.hid,power=u.infantrypower+u.cavalrypower,casubno=u.subno,empirename=u.empirename,minusstr=uw.minusstate,allyupbound=u.allyupbound,frienduserid=u.userid,city_id=uw.city_id,visited=i,corn=bonus,stri=readstr,friends=u.treasurebox,lev=u.lev,nobility=u.nobility,treasurenum=u.treasurenum,time=int(time.mktime(time.localtime())-time.mktime(beginTime)))
        except InvalidRequestError:
            print "error visit " + str(uu.userid) + ' ' + str(otherid)
            if visit!=None:
                visit.visited=1
            uu.corn=uu.corn+bonus#
            dv.visitnum=dv.visitnum+1
            uu.visitnum=dv.visitnum+1
            try:
                ca=DBSession.query(Card).filter_by(uid=u.userid).one()
                cardlist.append(ca.logincard)
            except:
                cardlist=[]            
            try:
                addnews(u.userid,uu.otherid,0,t,uu.user_kind)#2011.7.13:add news
            except:
                print "no such user" 
            if u == None or uu == None:
                return dict(id=0, reason="error no such user") 
            return dict(loginNum = u.logincard, money = u.corn, id=otherid, cardlist=cardlist,monsterdefeat=u.monsterdefeat,hid=u.hid,power=u.infantrypower+u.cavalrypower,casubno=u.subno,empirename=u.empirename,minusstr=uw.minusstate,frienduserid=u.userid,city_id=uw.city_id,visited=0,corn=85+15*(dv.visitnum),stri=readstr,friends=u.treasurebox,lev=u.lev,nobility=u.nobility,treasurenum=u.treasurenum,time=int(time.mktime(time.localtime())-time.mktime(beginTime)))
    @expose('json')
    def sell(self,user_id,city_id,grid_id):#对外接口，卖建筑物sell building#operationalData:update;businessWrite:query->update
        try:
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            
            if p.ground_id >=1000 and p.ground_id < 1100:
                return dict(id=0, reason='dragon can not be sold')
            if p.ground_id >= 420 and p.ground_id <= 424:
                lev = p.ground_id - 420
                i = 0
                while i <= lev:
                    u.populationupbound -= friendGod[i][4]
                    i += 1
                #h f c exp
                #u.food += friendGod[lev][1]/4
                cornAdd = [2500, 5000, 10000, 20000, 40000]
                u.corn += cornAdd[lev]
                    #todo reduce corn and food 
                DBSession.delete(p)
                return dict(id=1, result="sell friendGod suc", grid=grid_id)
            if p.ground_id >=600 and p.ground_id <= 605:
                print "sell statue"+" "+str(p.ground_id)
                index = p.ground_id - 600
                if statuebuilding[index][1]>0:
                    u.corn += statuebuilding[index][1]/4
                if statuebuilding[index][1]<0:
                    u.corn += statuebuilding[index][1]*(-500)
                u.labor_num -= statuebuilding[index][3]
                DBSession.delete(p)
                DBSession.flush()
                print "sell suc"
                return dict(id=1, result="sell statue suc", grid=grid_id)

            lis=getGround_id(p.ground_id)
            if lis==None:
                return dict(id=0)
            else:
                if p.ground_id>=1 and p.ground_id<=99:
                    u.labor_num=u.labor_num-lis[2]
                elif p.ground_id>=200 and p.ground_id<=299:
                    if (p.ground_id-200)%3==0:
                        u.labor_num=u.labor_num-lis[2]
                    elif (p.ground_id-200)%3==1:
                        lisx=getGround_id(p.ground_id-1)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]
                    elif (p.ground_id-200)%3==2:
                        lisx=getGround_id(p.ground_id-1)
                        lisy=getGround_id(p.ground_id-2)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]-lisy[2]
                elif p.ground_id>=300 and p.ground_id<399:
                    if (p.ground_id-300)%3==0:
                        u.labor_num=u.labor_num-lis[2]
                    elif (p.ground_id-300)%3==1:
                        lisx=getGround_id(p.ground_id-1)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]
                    elif (p.ground_id-300)%3==2:
                        lisx=getGround_id(p.ground_id-1)
                        lisy=getGround_id(p.ground_id-2)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]-lisy[2]
                elif p.ground_id>=400 and p.ground_id<420:
                    
                    if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412 or p.ground_id==416:
                        u.food_god_lev=0                                
                    elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413 or p.ground_id==417:

                        u.person_god_lev=0
                    elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414 or p.ground_id==418:
                                                      
                        u.wealth_god_lev=0
                    else:
                        u.war_god_lev=0                  
                else:
                    x=0     
                if p.ground_id>=400 and p.ground_id<420 and int((p.ground_id-400)/4)==0:
                    u.populationupbound=u.populationupbound-250
                elif p.ground_id>=400 and p.ground_id<420 and int((p.ground_id-400)/4)==1:
                    u.populationupbound=u.populationupbound-500
                elif p.ground_id>=400 and p.ground_id<420 and int((p.ground_id-400)/4)==2:
                    u.populationupbound=u.populationupbound-750
                elif p.ground_id>=400 and p.ground_id<420 and int((p.ground_id-400)/4)==3:
                    u.populationupbound=u.populationupbound-1000  
                elif p.ground_id>=400 and p.ground_id<420 and int((p.ground_id-400)/4)==4:
                    u.populationupbound=u.populationupbound-1250  
                lis1=[]                 
                if lis[0]>0:
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.corn=u.corn+lis[0]/4
                    elif p.ground_id>=500 and p.ground_id<=599:
                        u.corn=u.corn+lis[0]/4
                    elif p.ground_id>=400 and p.ground_id<420:
                        if p.ground_id<=403:
                            u.corn=u.corn+2500
                        elif p.ground_id<=407:
                            u.corn=u.corn+5000
                        elif p.ground_id<=411:
                            u.corn=u.corn+10000
                        elif p.ground_id<=415:
                            u.corn=u.corn+20000
                        else:
                            u.corn=u.corn+40000
                    elif p.ground_id>=100 and p.ground_id<=199:    
                        if (p.ground_id-100)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-100)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-100)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=200 and p.ground_id<=299:
                        if (p.ground_id-200)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-200)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-200)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=300 and p.ground_id<=399:
                        if (p.ground_id-300)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-300)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-300)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4                                                                                          
                else:
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.corn=u.corn+500*(-1*lis[0])
                    elif p.ground_id>=500 and p.ground_id<=599:
                        u.corn=u.corn+500*(-1*lis[0])                        
                    elif p.ground_id>=400 and p.ground_id<=499:
                        if p.ground_id<=403:
                            u.corn=u.corn+2500
                        elif p.ground_id<=407:
                            u.corn=u.corn+5000
                        elif p.ground_id<=411:
                            u.corn=u.corn+10000
                        elif p.ground_id<=415:
                            u.corn=u.corn+20000
                        else:
                            u.corn=u.corn+40000
                    elif p.ground_id>=100 and p.ground_id<=199:    
                        if (p.ground_id-100)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis[0])
                        elif (p.ground_id-100)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                                #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-100)%3==2:
                            lis1=getGround_id(p.ground_id-2)
                            if lis1[0]>0:
                                #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=200 and p.ground_id<=299:
                        if (p.ground_id-200)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis[0])
                        elif (p.ground_id-200)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-200)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=300 and p.ground_id<=399:
                        if (p.ground_id-300)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis[0])
                        elif (p.ground_id-300)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-300)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4                                                                  
                if u.labor_num<0:
                    u.labor_num=0
                if p.ground_id>=500 and p.ground_id <=599:
                    u.populationupbound=u.populationupbound-decorationbuild[p.ground_id-500][1]
                DBSession.delete(p)
                DBSession.flush()
                return  dict(id=1)
        except InvalidRequestError:
            return dict(id=0)   
    ###############地图相关
    @expose('json')
    def insert2(self,mapid):#Map:update
        war=None
        i=0
        mapid=int(mapid)
        try:
            c=DBSession.query(Map).filter_by(mapid=mapid).one()
            c.num=c.num+1
            try:
                war=DBSession.query(warMap).filter_by(mapid=mapid).order_by(warMap.gridid).all()
                if war!=None and len(war)!=0:
                    k=0
                    while k<=len(war)-1:
                        if war[k].gridid<=i:
                            i=war[k].gridid+1
                        k=k+1
                elif len(war)==0:
                    return dict(id=777)
                else:
                    return dict(id=666)
            except InvalidRequestError:
                return dict(id=888)                 
            return dict(i=i)
        except InvalidRequestError:
            return dict(i=-1)        
    global getGid
    def getGid(removes, kind):
        allNum = list(set(range(0, mapKind[kind])) - set(removes))
        rand = random.randint(0, len(allNum)-1)
        return [allNum[rand], allNum[(rand+1)%len(allNum)]]#myGid myEmpty
    global EmptyLev
    #inf cav coin food wood rock pro1/hour
    EmptyLev = [[100, 100,   10000, 1000, 100, 100,   100, 10, 1, 1],
                [100, 100,   20000, 2000, 200, 200,   100, 10, 1, 100],
                [100, 100,   100, 100, 100, 100,   100, 100, 100, 100],
                [100, 100,   100, 100, 100, 100,   100, 100, 100, 100],
                [100, 100,   100, 100, 100, 100,   100, 100, 100, 100],
                [100, 100,   100, 100, 100, 100,   100, 100, 100, 100],
            ]
    global moveMap
    def moveMap(uid):
        user = checkopdata(uid)
        myMap = DBSession.query(warMap).filter_by(userid = uid).one()
        #remove all empty
        empty = DBSession.query(EmptyCastal).filter_by(uid = uid).all()
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        print "collect my empty resource"
        for e in empty:
            e.uid = -1
            proTime = curTime - e.lastTime
            coinGen = proTime * EmptyLev[empty.lev][6]/2 
            foodGen = proTime * EmptyLev[empty.lev][7]/2
            woodGen = proTime * EmptyLev[empty.lev][8]/2
            stoneGen = proTime * EmptyLev[empty.lev][9]/2
            user.coin += coinGen
            user.food += foodGen
            user.wood += woodGen
            user.stone += stoneGen
            user.infantrypower += e.inf
            user.cavalrypower += e.cav
        print "find New map"
        #fetch a new map and nearby empty
        kind = user.nobility + 1
        #maps = DBSession.query(warMap).from_statement("select mapid, num from (select mapid, count(*) as num from warMap where map_kind=:kind group by mapid) as temp where num < :num ").params(kind=kind, num = mapKind[kind]).all()
        maps = DBSession.query(Map).filter_by(map_kind=kind).filter(Map.num < mapKind[kind]).all()
        for m in maps:
            empty = DBSession.query(EmptyCastal.gid).filter_by(mid = m.mapid).order_by(EmptyCastal.gid).all()
            cities = DBSession.query(warMap.gridid).filter_by(mapid = m.mapid).order_by(warMap.gridid).all()
            if len(empty) > len(cities):#insert me
                print "just insert me"
                gids = []
                for e in empty:
                    gids.append(e[0])
                for c in cities:
                    gids.append(c[0])
                gids.sort()
                m.num += 1
                myGid = (getGid(gids, kind))
                myMap.mapid = m.mapid
                myMap.gridid = myGid[0]
                myMap.map_kind += 1
                return [myGid[0], m.mapid]
            elif m.num < (mapKind[kind]-1):#insert 2
                print "insert me and empty"
                gids = []
                for e in empty:
                    gids.append(e[0])
                for c in cities:
                    gids.append(c[0])
                gids.sort()
                myGid = getGid(gids, kind)
                myMap.mapid = m.mapid
                myMap.gridid = myGid[0]
                myMap.map_kind += 1
                m.num += 2
                rand = random.randint(0, len(EmptyLev)-1)
                emptyCastal = EmptyCastal(uid=-1, mid = m.mapid, gid=myGid[1], attribute = rand, inf = EmptyLev[rand][0], cav = EmptyLev[rand][1])
                DBSession.add(emptyCastal)

                return [myGid[0], m.mapid]
        print "create new map to insert me and empty"
        #alloc new Map
        rand = random.randint(0, mapKind[kind]-1)
        newMap = Map(map_kind=kind, num=2)
        DBSession.add(newMap)
        DBSession.flush()
        print "mapid ", newMap.mapid
        
        myMap.mapid = newMap.mapid
        myMap.gridid = rand
        myMap.map_kind += 1

        rand = random.randint(0, len(EmptyLev)-1)
        emptyCastal = EmptyCastal(uid=-1, mid = newMap.mapid, gid = (rand+1)%mapKind[kind], attribute = rand, inf = EmptyLev[rand][0], cav = EmptyLev[rand][1])
        DBSession.add(emptyCastal)
        return [myMap.gridid, newMap.mapid]

    def getCity(city_id):
        s=''
        try:
            i=0
            cid=int(city_id)
            cset=DBSession.query(businessWrite).filter_by(city_id=cid).all()
            for c in cset:
                if i==0:
                    s=s+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
                    i=1
                else :
                    s=s+';'+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
        except InvalidRequestError:
            return ''
        return s
    @expose('json')
    def readAll(self, city_id):
        read(city_id)
        return dict(id=1)
    ###############
    def read(city_id):# 向businessread表中写入数据
        """
        try:
            s=''
            i=0
            cid=int(city_id)
            cset=DBSession.query(businessWrite).filter_by(city_id=cid).all()
            for c in cset:
                if i==0:
                    s=s+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
                    i=1
                else :
                    s=s+';'+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
            try:
                cc=DBSession.query(businessRead).filter_by(city_id=cid).one()
                #return dict(id=3,s=cc.layout)
                cc.layout=s
                return 1
            except InvalidRequestError:
                newread=businessRead(city_id=cid,layout=s)
                DBSession.add(newread)
                return 2
        except InvalidRequestError:
            return 0
        """
    @expose('json')
    def changename(self,userid,newname):#对外接口，更改领地名
        #u=DBSession.query(operationalData).filter_by(userid=int(userid)).one()
        u=checkopdata(userid)#cache
        u.empirename=newname
        replacecache(userid,u)#cache
        return dict(id=1,newname=newname)
    @expose('json')
    def newcomplete(self,uid,level):#对外接口，新手任务
        try:
            level=int(level)
            print "new comp " + str(uid) + ' ' + str(level)
            #user=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            user=checkopdata(uid)#cache
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            war=DBSession.query(warMap).filter_by(userid=int(uid)).one()
            if level==1:        
                user.newcomer=level
                user.corn=950
                user.exp=5
                user.cae=1
                user.food=120
                user.population=380
                user.labor_num=280
                replacecache(uid,user)#cache
                return dict(id=user.newcomer)
            elif level==2:
                user.newcomer=level
                user.corn=2950
                user.food=90
                user.cae=3
                user.exp=20
                user.lev=user.lev+1
                user.population=user.population+10
                try:
                    n=DBSession.query(businessWrite).filter_by(city_id=war.city_id).filter_by(grid_id=573).one()
                    n.ground_id=100
                    n.producttime=t
                    n.finish=0
                except InvalidRequestError:
                
                    newbuilding=businessWrite(city_id=war.city_id,ground_id=100,grid_id=573,object_id=-1,producttime=t,finish=0)
                    DBSession.add(newbuilding)
                try:
                    n1=DBSession.query(businessWrite).filter_by(city_id=war.city_id).filter_by(grid_id=570).one()
                    n1.ground_id=300
                    n1.producttime=t
                    n1.finish=1
                except InvalidRequestError:
                
                    newbuilding1=businessWrite(city_id=war.city_id,ground_id=300,grid_id=570,object_id=-1,producttime=t,finish=1)
                    DBSession.add(newbuilding1)
                
                read(war.city_id)
            
            else:
                user.newcomer=level
                user.exp=50#50+
                user.lev=user.lev+1
                user.corn=5550
                user.cae=6
                task=tasknew(user.userid)
                user.monstertime=t+1800
                user.monsterlist=''
                #user.food=190
                #user.infantrypower=60
                #user.labor_num=0
                #user.population=160
                user.corn=user.corn+3000
                user.currenttask=task[1]
                user.taskstring='0'
                user.warcurrenttask='0'
                user.wartaskstring='0'
                user.loginnum=user.loginnum+1
                ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()
                ds.datesurprise=1
                try:
                    cd=DBSession.query(Card).filter_by(uid=user.userid).one()
                    cd.logincard=cd.logincard+1
                except:
                    xx=1
                nup=[]
                try:
                    x=DBSession.query(Papayafriend).filter_by(papayaid=user.otherid).filter_by(user_kind=user.user_kind).all()
                    for xx in x:
                        xx.lev=3
                except InvalidRequestError:
                    x=[]              
            replacecache(uid,user)#cache
            return dict(task=task[0],id=user.newcomer)
        except :
            return dict(id=0)
    ###############
    ###############新闻相关
    def addnews(uid,fpapayaid,kind,time,fuser_kind):#添加新闻函数
        news=News(uid=uid,fpapayaid=fpapayaid,kind=kind,time=time,fuser_kind=fuser_kind)
        DBSession.add(news)
    @expose('json')
    def getnewsnum(self,uid):#获取新闻总数
        try:
            nlist=[]
            uid=int(uid)
            newsset=DBSession.query(News).filter_by(uid=uid)
            for n in newsset:
                nlist.append(n.uid)
            i=len(nlist) 
            return dict(id=i)    
        except:
            return dict(id=0)
    @expose('json')
    def getnews(self,uid,off,size):#对外接口，获取新闻
        uid=int(uid)
        newslist=[]
        nl=[]
        num=11
        x=0 
        off=int(off)
        size=int(size)       
        try:
            newsset=DBSession.query(News).filter_by(uid=uid).order_by(News.id)
            for n in newsset:
                ntemp=[n.fpapayaid,n.kind,n.time]
                nl.append(ntemp)    
            if len(nl)==0 or nl==None :
                return dict(id=0)
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            i=off
            l1=size+off
            if l1>len(nl):
                l1=len(nl)
            while i<l1:
                n1=[nl[i][0],nl[i][1],nl[i][2]]
                i=i+1
                newslist.append(n1)
            #return dict(id=1)
            return dict(time=u.logintime,news=newslist)
                
        except InvalidRequestError:
            return dict(id=0) 
    ###############  
  
         
    @expose('json')
    def datarefresh(self,uid):
        try:
            u=checkopdata(uid)
            s=DBSession.query(warMap).filter_by(userid=uid).one()#获取city_id
            st = getCity(s.city_id)
              
            return dict(id=1,stri=st,monsterdefeat=u.monsterdefeat,monsterstr=u.monsterlist,infantrypower=u.infantrypower,cavalrypower=u.cavalrypower,exp=u.exp,corn=u.corn,cae=u.cae,lev=u.lev,nobility=u.nobility,wood=u.wood,stone=u.stone,labor_num=u.labor_num,population=u.population,populationupbound=u.populationupbound)
        except:
            return dict(id=0, reason = "city not find")
             
    @expose('json')
    def updateppyname(self,uid,ppyname):
        try:
            u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u.papayaname=ppyname
            return dict(id=1)
        except:
            return dict(id=0)

    @expose('json')
    def changecard(self,userid,cardnum,type):
        cardtype=int(type)
        cardnum=int(cardnum)
        userid=int(userid)
        try:
            card=DBSession.query(Card).filter("uid=:uid").params(uid=userid).one()
            if cardtype==0:
                card.foodcard=cardnum
            elif cardtype==1:
                card.fortunecard=cardnum
            elif cardtype==2:
                card.popcard=cardnum
            elif cardtype==3:
                card.warcard=cardnum
            elif cardtype==4:
                card.friendcard=cardnum
            return dict(id=1,card=card)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    #user_kind 
    def logsign(self,papayaid,user_kind,md5):# 对外接口，登陆注册login if signed or sign;operationalData:query
        print "login from 1"
        user=None
        oid=papayaid#papayaid改为string类型
        user_kind=int(user_kind)
        logintime=int(time.mktime(time.localtime())-time.mktime(beginTime))
        lbonus=-1
        wargodtime=-1
        wealthgodtime=-1
        popgodtime=-1
        foodlost=0
        src=papayaid+'-'+md5string
        md51=hashlib.md5(src).hexdigest()
        card=None
        cardlist=[]#卡片列表
        if md51!=md5:
            return dict(md51=md51,id=md5)
        try:
            ruser=DBSession.query(operationalData).filter_by(otherid=oid).filter_by(user_kind=user_kind).one()
            user=checkopdata(ruser.userid)
            ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()
            bonus=loginBonus(user)#获取登录奖励
            lbonus=bonus
            s=DBSession.query(warMap).filter_by(userid=user.userid).one()#获取city_id
            stt= getCity(s.city_id)

            corn=user.corn
            cae=user.cae
            population=user.population
            labor_num=user.labor_num
            exp=user.exp
            fo=user.food
            tasklist=[]
            wonBonus = 0
            wonNum = 0
            try:
                vict = DBSession.query(Victories).filter_by(uid = user.userid).one()
                wonNum = vict.won
                dif = logintime / 86400 - user.logintime/86400
                if dif >= 1:
                    nob = user.nobility
                    perReward = 300 + nob*50
                    if vict.won > 0:
                        wonBonus = vict.won * perReward
                        user.corn += wonBonus
                        print "user colonial reward = " + str(vict.won * perReward)
            except:
                print "colonial reward fail"
            print "wonBonus "+str(wonBonus)+' ' +str(wonNum)
            user.logintime=logintime
            lisa=[]
            try:
                ally=DBSession.query(Ally).filter_by(uid=user.userid)
                for a in ally :
                    papaya=checkopdata(a.fid)#cache
                    lisa.append(papaya.otherid)
                    lisa.append(papaya.nobility*3+papaya.subno)
                    
            except InvalidRequestError:
                lisa=[]
            ######获得卡片数据
            try:
                card=DBSession.query(Card).filter_by(uid=user.userid).one()
                cardlist.append(card.logincard)
                cardlist.append(card.foodcard)
                cardlist.append(card.fortunecard)
                cardlist.append(card.popcard)
                cardlist.append(card.warcard)
                cardlist.append(card.friendcard)
            except:
                card=None
            #######卡片数量列表

            #cardlist.append(card.logincard)
            ng=[]
            try:
                ng=DBSession.query(Gift).filter_by(fid=user.otherid).filter_by(received=0).all()#giftstring(user.otherid)
                giftstr=len(ng)
                
                if giftstr>100:
                    giftstr=100
                    
                    
            except InvalidRequestError:
                giftstr=0
            minusstr=s.minusstate
            replacecache(user.userid,user)
            ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()   
            if user.war_god==1:
                wargodtime=3600-(logintime-user.wargodtime)
            elif user.war_god==2:
                wargodtime=21600-(logintime-user.wargodtime)
            elif user.war_god==3:
                wargodtime=86400-(logintime-user.wargodtime)
            else:
                wargodtime=user.wargodtime
            if wargodtime<=0:
                user.war_god=0
                user.wargodtime=0
                wargodtime=0
            if user.war_god_lev == 0:
                wargodtime = -1

            if user.person_god==1:
                popgodtime=3600-(logintime-user.popgodtime)
            elif user.person_god==2:
                popgodtime=21600-(logintime-user.popgodtime)
            elif user.person_god==3:
                popgodtime=86400-(logintime-user.popgodtime)
            else:
                popgodtime=user.popgodtime
            if popgodtime<=0:
                user.pop_god=0
                user.popgodtime=0 
                popgodtime=0
            if user.person_god_lev == 0:
                popgodtime = -1

            if user.food_god==1:
                foodgodtime=3600-(logintime-user.foodgodtime)
            elif user.food_god==2:
                foodgodtime=21600-(logintime-user.foodgodtime)
            elif user.food_god==3:
                foodgodtime=86400-(logintime-user.foodgodtime)
            else:
                foodgodtime=user.foodgodtime
            if foodgodtime<=0:
                user.food_god=0
                user.foodgodtime=0 
                foodgodtime=0
            if user.food_god_lev == 0:
                foodgodtime = -1

            if user.wealth_god==1:
                wealthgodtime=3600-(logintime-user.wealthgodtime)
            elif user.wealth_god==2:
                wealthgodtime=21600-(logintime-user.wealthgodtime)
            elif user.wealth_god==3:
                wealthgodtime=86400-(logintime-user.wealthgodtime)
            else:
                wealthgodtime=user.wealthgodtime
            if wealthgodtime<=0:
                user.wealth_god=0
                user.wealthgodtime=0 
                wealthgodtime=0 
            if user.wealth_god_lev == 0:
                wealthgodtime = -1

            task=-1
            if user.currenttask=='' or user.currenttask==None or user.currenttask=='-1' or int(user.currenttask)<0:
                task=-1
            else:
                task=taskbonus[int(user.currenttask)][0]#id for client data base store current task  
            wartask=-1 
            if user.warcurrenttask=='' or user.warcurrenttask==None or user.warcurrenttask=='-1' or int(user.warcurrenttask)<0:
                wartask=-1
            else:
                wartask=wartaskbonus[int(user.warcurrenttask)][0]
            sub=0
            try:
                v=DBSession.query(Victories).filter_by(uid=user.userid).one()
                sub=recalev(user,v)
            except:
                sub=-1
            #loginNum how many time login continuous
            #if ds.monfood < 2:
            #    foodlost = 0
            #else:
            #    foodlost = 1
            if user.newcomer<3:
                return dict(loginNum = user.logincard, wonNum=wonNum, wonBonus = wonBonus, sub=sub,wartaskstring=user.wartaskstring,wartask=wartask,ppyname=user.papayaname,cardlist=cardlist,monsterdefeat=user.monsterdefeat,monsterid=user.monster,foodlost=ds.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,newstate=user.newcomer,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftnum=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)    
            if user_kind==0:
                return dict(loginNum = user.logincard, wonNum=wonNum, wonBonus = wonBonus, sub=sub,wartaskstring=user.wartaskstring,wartask=wartask,ppyname=user.papayaname,cardlist=cardlist,monsterdefeat=user.monsterdefeat,monsterid=user.monster,foodlost=ds.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,tasklist=tasklist,taskstring=user.taskstring,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftnum=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)
            else:
                return dict(loginNum = user.logincard, wonNum = wonNum, wonBonus = wonBonus,sub=sub,wartaskstring=user.wartaskstring,wartask=wartask,ppyname=user.papayaname,cardlist=cardlist,monsterdefeat=user.monsterdefeat,monsterid=user.monster,hid=user.hid,foodlost=ds.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,headid=user.hid,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,invitestring=user.invitestring,tasklist=tasklist,taskstring=user.taskstring,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftnum=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)
                    
        except InvalidRequestError:
            newuser=operationalData(labor_num=280,population=380,exp=0,corn=1000,cae=1,nobility=-1,infantry1_num=30,cavalry1_num=0,scout1_num=0,person_god=0,wealth_god=0,food_god=0,war_god=0,user_kind=user_kind,otherid=oid,lev=1,empirename='我的领地',food=100)
            DBSession.add(newuser)
            newuser = DBSession.query(operationalData).filter_by(otherid = oid).one()
            c1=DBSession.query('LAST_INSERT_ID()')
            c1=c1[0]
            gi=0
            mi=0
            nuid=c1[0]
            
            nu=DBSession.query(operationalData).filter_by(userid=nuid).one()
            nu.logintime=logintime
            nu.signtime=logintime
            newvictories=Victories(uid=c1[0],won=0,lost=0)
            DBSession.add(newvictories)
            nu.infantrypower=60
            nu.infantrypower=30
            nu.monsterlist='0,7'
            nwMap=warMap(c1[0],-1,-1,0)
            DBSession.add(nwMap)

            gi=-1
            mi=-1

            cid = DBSession.query(warMap).filter_by(userid=newuser.userid).one()
            inistr=''
            inistr=inistr+INITIALSTR2+str(logintime)+',0;'+'100,575,-1,'+str(logintime-86400)+',1;300,570,-1,'+str(logintime-86400)+',1;1,690,0,'+str(logintime-86400)+',1';
            
            nbw=businessWrite(city_id=cid.city_id,ground_id=0,grid_id=455,object_id=0,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=491,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=527,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)            
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=528,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=200,grid_id=566,object_id=-1,producttime=logintime,finish=0)#bingying
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=567,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=531,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)            
            nbw=businessWrite(city_id=cid.city_id,ground_id=520,grid_id=568,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=100,grid_id=575,object_id=-1,producttime=logintime-86400,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=571,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=515,grid_id=493,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=606,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=607,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=608,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=609,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=610,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=611,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=612,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=613,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=614,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=615,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=616,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw) 
            nbw=businessWrite(city_id=cid.city_id,ground_id=530,grid_id=646,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=651,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw) 
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=691,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=731,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=503,grid_id=771,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)                                    
            nbw=businessWrite(city_id=cid.city_id,ground_id=1,grid_id=688,object_id=-1,producttime=0,finish=1) 
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=1,grid_id=690,object_id=0,producttime=logintime-86400,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid.city_id,ground_id=300,grid_id=570,object_id=-1,producttime=logintime-86400,finish=1)  
            DBSession.add(nbw)       
            ds=Datesurprise(uid=nu.userid,datesurprise=0)
            DBSession.add(ds)
            dv=Datevisit(uid=nu.userid,visitnum=0)
            DBSession.add(dv)
            ####卡片
            nc=Card(uid=nuid)
            DBSession.add(nc)
            ####卡片

            try:
                nuf=DBSession.query(Papayafriend).filter_by(papayaid=papayaid).filter_by(user_kind=int(user_kind)).all()
                for x in nuf:
                    x.lev=1
                    d=DBSession.query(operationalData).filter_by(userid=x.uid).one()
                    try:
                        xx=DBSession.query(Papayafriend).filter_by(uid=nu.userid).filter_by(papayaid=d.userid).one()
                    except InvalidRequestError:
                        xxx=Papayafriend(uid=nu.userid,papayaid=d.otherid,lev=d.lev,user_kind=d.user_kind)
                        DBSession.add(xxx)
            except InvalidRequestError:
                x=0
            #should not do internet connection which will block
            conn = httplib.HTTPConnection(SERVER_NAME)
            #user_id is a var
            url_send = "/a/misc/wonderempire_event?uid="+papayaid+"&event=1"
            conn.request('GET',url_send)
            res = conn.getresponse()
            #userdata = json.read(res.read())
            if res.status == 200:
                print "succeeded!"
            else:
                print "failed!"
            return dict(wonNum = 0, wonBonus = 0, ppyname=nu.papayaname,infantrypower=nu.infantrypower,cavalrypower=nu.cavalrypower,castlelev=nu.castlelev,newstate=0,popupbound=nu.populationupbound,wood=nu.wood,stone=nu.stone,specialgoods=nu.specialgoods,time=nu.logintime,labor_num=280,nobility=0,population=380,food=100,corn=1000,cae=nu.cae,exp=0,stri=inistr,id=c1[0],city_id=cid.city_id,mapid=mi,gridid=gi)
    #check won in map check occupation
    @expose('json')
    def upgrademap(self,userid):#对外接口，爵位升级，进入新地图 user update and go to new map#OccupationData:query operationalData:query->update;warMap:update;Victories:update
        try:
            print "upgrade map"
            userid=int(userid)
            u=checkopdata(userid)#cache
            v=DBSession.query(Victories).filter_by(uid=userid).one()
            #need how many to upgrade 
            min = calev(u, v)
            print "cur minus" + str(min[1])
            if min[1] > 0:
                print "need more ene to defeat " + str(min[0]) + ' ' + str(min[1])
                return dict(id = 0)

            print "update occupy and warmap"
            o=DBSession.query(Occupation).filter_by(masterid=userid)
            
            if u.nobility==NOBILITYUP:
                return dict(id=0)
            print "remove all occupy relationship"
            for oo in o:
                DBSession.delete(oo)
            
            print "remove all current running battle"
            curBattle = DBSession.query(Battle).filter(Battle.finish==0).filter("uid=:uid0 or enemy_id=:uid1").params(uid0=int(userid), uid1=int(userid)).all();
            for b in curBattle:
                print 'remove b ' + str(b.uid) + ' ' + str(b.enemy_id) + ' ' +str(b.powerin) + ' ' + str(b.powerca) 
                if b.finish != 0:
                    continue
                b.finish = 3#cancel
                attacker = checkopdata(b.uid)
                attacker.infantrypower += b.powerin
                attacker.cavalrypower += b.powerca
            allBattle = DBSession.query(Battle).filter(Battle.finish!=0).filter("uid=:uid0 or enemy_id=:uid1").params(uid0=int(userid), uid1=int(userid)).all();
            for b in allBattle:
                if b.finish != 0:
                    DBSession.delete(b)
            #move to new map
            c = moveMap(userid) 
            print "moveMap " + str(c)
            u.corn=u.corn+nobilitybonuslist[u.nobility][0]
            u.food=u.food+nobilitybonuslist[u.nobility][1]
            u.wood=u.wood+nobilitybonuslist[u.nobility][2]
            u.stone=u.stone+nobilitybonuslist[u.nobility][3]
            
            cur = int(time.mktime(time.localtime()) - time.mktime(beginTime))
            #24 hours protect
            u.protecttype = 2
            u.protecttime = cur
            
            no=u.nobility
            u.allyupbound=u.allyupbound+allyup[no+1]-allyup[no]
            u.nobility += 1
            print "new nobility " + str(u.nobility)
            v.lostinmap=0
            v.woninmap=0
            v.delostinmap=0
            v.dewoninmap=0
            
            u.battleresult=''
            u.EmptyResult = ''
            u.subno=0
            min = calev(u, v)
            print "next leve need minus " + str(min[1])
            return dict(id=1, mapid=c[1],gridid=c[0],sub=min[0], minus = min[1])
        except InvalidRequestError:
            return dict(id=0)
    
    @expose('json')
    def adddefence(self,uid,defencenum,type):#对外接口，增加城池防御力
        type=int(type)
        uid=int(uid)
        food=0
        wood=0
        stone=0
        cae=0
        nobility=0
        defencenum=int(defencenum)
        try:
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            nobility=u.nobility
            x=defenceplist[nobility][1]
            if type==0:
                cae=int((defencenum+100-1)/100)
                if u.cae-cae>=0:
                    u.defencepower=u.defencepower+defencenum
                    u.cae=u.cae-cae
                    
                    print inspect.stack()[0]
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                corn=100*defencenum
                food=5*defencenum
                if u.corn-corn>=0 and u.food-food>=0:
                    u.corn=u.corn-corn
                    u.food=u.food-food
                    u.defencepower=u.defencepower+defencenum
                    replacecache(uid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0) 
        except InvalidRequestError:
            return dict(id=0)
    def allyhelp(uid,type,poweru):#计算盟友战斗力
        uid=int(uid)
        fullpower=0
        #enemy_id=int(enemy_id)
        type=int(type)#0:attack,1:defence
        poweru=int(poweru)
        try:
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            #ba=DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id=enemy_id).one()
            allyset=DBSession.query(Ally).filter_by(uid=uid)

            for a in allyset :
                fid=a.fid
                #f=DBSession.query(operationalData).filter_by(userid=fid).one()
                f=checkopdata(fid)#cache
                if int((returnsentouryoku(f)+20-1)/20)>int((poweru+10-1)/10):
                    fullpower += int((poweru+10-1)/10)
                else:
                    fullpower += int((returnsentouryoku(f)+20-1)/20)
            return fullpower
        except InvalidRequestError:
            return 0 

    #check if attack exist
    @expose('json')
    def attackspeedup(self,uid,enemy_id):
        print "speed up " + str(uid) + ' ' + str(enemy_id)
        uid=int(uid)
        enemy_id=int(enemy_id)
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        #if uid == enemy_id:
        #    return dict(id=0, reason='self attack self')
        try:
            #f=checkopdata(enemy_id)
            ub=DBSession.query(Battle).filter("uid=:uid and enemy_id=:ene and finish = 0").params(uid=uid, ene=enemy_id).one()
            tl=ub.timeneed-(t-ub.left_time)
            hour = 3600
            cae = 0
            if tl < 0:#finish yet
               cae = 0
            elif tl < 3 * hour:
               cae = 2
            elif tl < 6 * hour:
               cae = 4
            elif tl < 9 * hour:
               cae = 6
            else:
               cae = 10
            u=checkopdata(uid)
            
            if u.cae-cae>=0:
                u.cae=u.cae-cae  
                ub.timeneed=0
                print inspect.stack()[0]
                print "speed cae " + str(cae) + 'time ' + str(tl)
                return dict(id=1, caesars = cae)
            else:
                return dict(id=0, reason='cae')
        except:
            return dict(id=0, reason='no bat')
    @expose('json')
    def harvestEmpty(self, uid, cid):
        uid = int(uid)
        cid = int(cid)
        empty = DBSession.query(EmptyCastal).filter_by(cid=cid).one()
        user = checkopdata(uid)
        if empty.uid != uid:
            return dict(id=0, status = 0, reason='not your empty')
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        proTime = (curTime - empty.lastTime)*1.0/3600
        #not over limitation 10000
        if proTime >= 1.0:
            coinGen = int(min(proTime * EmptyLev[empty.attribute][6], 10000)) 
            foodGen = int(min(proTime * EmptyLev[empty.attribute][7], 10000))
            woodGen = int(min(proTime * EmptyLev[empty.attribute][8], 100))
            stoneGen = int(min(proTime * EmptyLev[empty.attribute][9], 100))
            user.corn += coinGen
            user.food += foodGen
            user.wood += woodGen
            user.stone += stoneGen
            empty.lastTime = curTime
            return dict(id=1, coinGen = coinGen, foodGen = foodGen, woodGen = woodGen, stoneGen = stoneGen, lastTime = curTime)
        return dict(id=0, status = 0, reason='protime< 3600')
        

    @expose('json')
    def callbackEmpty(self, uid, cid, inf, cav):
        uid = int(uid)
        cid = int(cid)
        inf = int(inf)
        cav = int(cav)
        empty = DBSession.query(EmptyCastal).filter_by(cid = cid).one()
        if empty.uid != uid:
            return dict(id=0, status = 0, reason='not your emptyCity')
        user = checkopdata(uid)
        inf = min(empty.inf, inf)
        cav = min(empty.cav, cav)
        empty.inf -= inf
        empty.cav -= cav
        empty.inf = max(empty.inf, 0)
        empty.cav = max(empty.cav, 0)
        user.infantrypower += inf
        user.cavalrypower += cav
        return dict(id=1, inf = inf, cav = cav)
    #enemy_id > 0 but battle < 0
    @expose('json')
    def withdrawEmpty(self, uid, enemy_id):
        battle = DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id = enemy_id).filter_by(finish=0).all() 
        if len(battle) == 0:
            return dict(id = 0, status = 0, reason = 'no battle')
        user = checkopdata(uid)
        battle.finish = 4#0 unfin 1suc 2 fail 3cancel 4withdraw
        user.infantrypower += battle.powerin
        user.cavalrypower += battle.powerca
        return dict(id = 1)
    #check if attack in battle 1
    #if occupy yet 2
    #if ene in protect state
    global attackEmpty
    def attackEmpty(uid, enemy_id, timeneed, infantry, cavalry):
        #enemy_id < 0
        battle = DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id=enemy_id).filter_by(finish = 0).all()
        if len(battle) > 0:
            return dict(id=0, status = 0, reason='attacking')
        user = checkopdata(uid)
        try:
            empty = DBSession.query(EmptyCastal).filter_by(cid=-enemy_id).one()
        except:
            return dict(id=0, status=1, reason='no this emptyC')
        if user.infantrypower >= infantry and user.cavalrypower >= cavalry:
            user.infantrypower -= infantry
            user.cavalrypower -= cavalry
            timeNow = int(time.mktime(time.localtime()) - time.mktime(beginTime))
            #replace old battle
            battle = DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id = enemy_id).filter(Battle.finish != 0).all()
            allypower=allyhelp(uid,0,infantry+cavalry)
            if len(battle) == 0:#create New
                nb = Battle(uid=uid, enemy_id=enemy_id, left_time = timeNow, timeneed=timeneed,  powerin = infantry, powerca = cavalry, power = infantry+cavalry, allypower = allypower)
                DBSession.add(nb)
            else:#replace
                nb = battle[0]
                nb.enemy_id = enemy_id
                nb.left_time = timeNow
                nb.timeneed = timeneed
                nb.finish = 0
                nb.powerin = infantry
                nb.powerca = cavalry
                nb.power = infantry + cavalry
                nb.allypower = allypower
            DBSession.flush()
            return dict(id=1)
        return dict(id=0, status = 2, reason = "power not enough")


    #if enemy_id < 0 attack empty castal
    @expose('json')
    def attack(self,uid,enemy_id,timeneed,infantry,cavalry):#对外接口，进攻
        uid=int(uid)
        enemy_id=int(enemy_id)
        timeneed=int(timeneed)
        infantry=int(infantry)
        cavalry=int(cavalry)
        if enemy_id < 0:
            return attackEmpty(uid, enemy_id, timeneed, infantry, cavalry)
        if uid == enemy_id:
            return dict(id=0, status = 4)
        try:
            occupy = DBSession.query(Occupation).filter_by(masterid=uid).filter_by(slaveid=enemy_id).one()
            print "you occupy him"
            return dict(id = 0, status = 2)
        except:
            print "no occupy data"

        u=checkopdata(uid)#cache
        f=checkopdata(enemy_id)
        myMap = DBSession.query(warMap.mapid).filter_by(userid = u.userid).one()
        eneMap = DBSession.query(warMap.mapid).filter_by(userid = f.userid).one()
        print "mymap " + str(myMap.mapid) + "enemap " + str(eneMap.mapid)
        if myMap.mapid != eneMap.mapid:
            return dict(id = 0, status = 3, reason = "not in same map")

        if checkprotect(f)>0:
            print "target in protect"
            pType = f.protecttype
            pTime = [7200, 28800, 86400]
            endt = pTime[pType] + f.protecttime
            return dict(id=0, status=0, endtime = endt)

        timeNow = int(time.mktime(time.localtime()) - time.mktime(beginTime))
        try:
            ub=DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id=enemy_id).one()
            if ub.finish == 0:
                return dict(id = 0, status = 1)

            u.infantrypower=u.infantrypower-infantry
            u.cavalrypower=u.cavalrypower-cavalry  
            ub.timeneed=timeneed
            ub.finish=0
            ub.left_time=timeNow
            ub.powerin=infantry
            ub.powerca=cavalry
            ub.power=infantry+cavalry
            allypower=allyhelp(uid,0,infantry+cavalry)
            ub.allypower=allypower
            print 'replace old battle info ' + str(uid)
            rep = 1
        except InvalidRequestError:
            print 'attack ' + str(uid) + ' ' + str(enemy_id) + ' timeneed ' + str(timeneed)
            u = checkopdata(uid)
            u.infantrypower=u.infantrypower-infantry
            u.cavalrypower=u.cavalrypower-cavalry   
            allypower=allyhelp(uid,0,infantry+cavalry)    
            nb=Battle(uid=uid,enemy_id=enemy_id,left_time=timeNow,timeneed=timeneed,powerin=infantry,powerca=cavalry,power=infantry+cavalry,allypower=allypower)
            DBSession.add(nb)
            rep = 0
        u.signtime = 0
        u.protecttime = -1
        u.protecttype = -1
        return dict(id=1, replace = rep)                                     
    def returnscout(u):#返回侦察兵数量
        scout=[]
        scout.append(u.scout1_num)
        scout.append(u.scout2_num)
        scout.append(u.scout3_num)
        return scout
    #all my empty
    @expose('json')
    def getEmpty(self, uid):
        uid = int(uid)
        empty = DBSession.query(EmptyCastal.cid, EmptyCastal.mid, EmptyCastal.gid, EmptyCastal.inf, EmptyCastal.cav, EmptyCastal.lastTime).filter_by(uid=uid).all()
        return dict(id=1, empties = empty)
    @expose('json')
    def detectEmpty(self, uid, cid, t):
        user = checkopdata(uid)
        scout = returnscout(user)
        cid = int(cid)
        t = int(t)
        try:
            empty = DBSession.query(EmptyCastal).filter_by(cid = cid).one()
        except:
            return dict(id=0, status = 2, reason = 'no this empty')
        if t <= 2:
            if scout[t] < 6:
                return dict(id=0, status = 0, reason='scout not enough')
        if t == 3:
            if user.cae < user.nobility+1:
                return dict(id=0, status = 1, reason='cae not enough')


        if t == 0:
            user.scout1_num -= 6
            return dict(id=1, inf = empty.inf, cav = empty.cav)
        elif t == 1:
            user.scout2_num -= 6
            battle = DBSession.query(Battle.uid, Battle.left_time, Battle.timeneed).filter_by(enemy_id=-cid).filter_by(finish = 0).order_by(desc(Battle.left_time)).all()
            curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
            blist = list(battle)[0:len(battle)/2]
            return dict(id=1, inf = empty.inf, cav = empty.cav, attack = blist)
        elif t == 2:
            user.scout3_num -= 6
            battle = DBSession.query(Battle.uid, Battle.left_time, Battle.timeneed).filter_by(enemy_id=-cid).filter_by(finish = 0).order_by(desc(Battle.left_time)).all()
            blist = list(battle)
            return dict(id=1, inf = empty.inf, cav = empty.cav, attack = blist)
        elif t == 3:
            user.cae -= user.nobility+1
            battle = DBSession.query(Battle.uid, Battle.left_time, Battle.timeneed, Battle.powerin, Battle.powerca).filter_by(enemy_id=-cid).filter_by(finish = 0).order_by(desc(Battle.left_time)).all()
            blist = list(battle)
            return dict(id=1, inf = empty.inf, cav = empty.cav, attack = blist)
        return dict(id = 0, status = 2, reason='no such detect')
    @expose('json')
    def detect(self,uid,enemy_id,type):#对外接口，侦察
        type=int(type)
        scout=[]
        num=[2,6,12,0]
        i=0
        k=3
        mark=0
        enemy_id=int(enemy_id)
        killed=0
        allypower=0
        try:
            u=checkopdata(uid)#cache
            scout=returnscout(u)
            m=random.randint(1,100)
            if type<=2 and scout[type]-6<0:
                return dict(id=0)
            if type==3 and u.cae-(u.nobility+1)<0:
                return dict(id=0)
            if type==4 and u.cae-1<0:
                return dict(id=0)
            if type==0:
                if m<=50:
                    killed=random.randint(1, 6)
                    u.scout1_num=u.scout1_num-killed
                    mark=1
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()
                replacecache(uid,u)#cache
                return dict(dead=killed,won=v.won,total=v.lost+v.won)
            elif type==1:
                if m<=65:
                    killed=random.randint(1, 6)
                    u.scout2_num=u.scout2_num-killed
                    mark=1
                #uv=DBSession.query(operationalData).filter_by(userid=enemy_id).one()
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()
                replacecache(uid,u)#cache
                return dict(dead=killed,won=v.won,total=v.won+v.lost,power=uv.infantrypower+uv.cavalrypower)
            elif type==2:
                if m<=80:
                    mark=1
                    killed=random.randint(1,6)
                    u.scout3_num=u.scout3_num-killed
                #uv=DBSession.query(operationalData).filter_by(userid=enemy_id).one()
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()  
                allypower=allyhelp(uv.userid,1,uv.infantrypower+uv.cavalrypower)  
                replacecache(uid,u)#cache            
                return dict(dead=killed,won=v.won,total=v.lost+v.won,power=uv.infantrypower+uv.cavalrypower,allynum=allypower)
            elif type==3:
                u.cae=u.cae-(u.nobility+1)
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()
                allypower=allyhelp(uv.userid,1,uv.infantrypower+uv.cavalrypower)      
                print inspect.stack()[0]

                return dict(won=v.won,total=v.lost+v.won,power=uv.infantrypower+uv.cavalrypower,citydefence=uv.defencepower,allynum=allypower)
            else:
                u.cae=u.cae-1
                ba=DBSession.query(Battle).filter_by(uid=enemy_id).filter_by(enemy_id=u.userid).one()
                power=ba.allypower
                print inspect.stack()[0]

                return dict(power=power)       
        except InvalidRequestError:
            return dict(id=0)                 
    def checkprotect(u):
        ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
        proTime = [7200, 28800, 86400]
        if u.protecttype==-1:
            return -1
        else:
            proType = u.protecttype
            if proType >= 0 and proType < len(proTime):
                if ti - u.protecttime > proTime[proType]:
                    u.protecttype = -1
                    return -1
                return proTime[proType] + u.protecttime
        return -1
    #0 1 2 3 newer protect
    @expose('json')
    def addprotect(self,uid,type):
        u=checkopdata(uid)
        type=int(type)
        ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
        price = [4999, 14999, 2]
        if u.protecttype != -1:
            return dict(id=0)
        if type < 0 or type >= 3:
            return dict(id=0, reason = "no such protect")
        suc = False
        if type == 0:
            if u.corn >= 4999:
                u.corn -= 4999
                suc = True
        elif type == 1:
            if u.corn >= 14999:
                u.corn -= 14999
                suc = True
        elif type == 2:
            if u.cae >= 2:
                u.cae -= 2
                suc = True
                print inspect.stack()[0]

        if suc:
            u.protecttype = type
            u.protecttime = ti
            return dict(id=1, result = 'protect type '+str(type))
        return dict(id=0, reason = 'unknown')  
    @expose('json')
    def battlerank(self,type,off,num,uid):
        rank1=[]
        rank2=[]
        rank3=[]
        off=int(off)
        num=int(num)
        type=int(type)
        uid=int(uid)
        try:
            if type==0:
                #rank1=DBSession.query(operationalData.otherid,operationalData.empirename,operationalData.nobility,operationalData.power).filter_by(order_by(operationalData.cae).order_by(operationalData.corn).all()
                rank1.sort(key=lambda x:(x.cae*1000+x.corn,x.lev))
                
                
                for n in rank1:
                    rank2.append([n.userid,n.otherid,n.cae,n.corn,n.lev])
                if rank2==None or len(rank2)==0:
                    return dict(id=0)   
                i=len(rank2)-1-off
                l1=len(rank2)-1-off-num
                if l1<0:
                    l1=0
                while i>l1:
                    rank3.append(rank2[i])
                    i=i-1                    
                return dict(rank=rank3)
            else:
                fl=DBSession.query(Papayafriend.papayaid).filter_by(uid=int(uid)).all()
                fll=[]
                rank2=[]
                for n in fl:
                    fll.append(n[0])
                rank1=DBSession.query(operationalData).filter(operationalData.otherid.in_(fll)).all()
                rank1.sort(key=lambda x:(x.cae*1000+x.corn,x.lev))
                for n in rank1:
                    rank2.append([n.userid,n.otherid,n.cae,n.corn,n.lev])
                if rank2==None or len(rank2)==0:
                    return dict(rank1=rank1,id=0)   
                i=len(rank2)-1-off
                l1=len(rank2)-1-off-num
                if l1<0:
                    l1=0
                while i>l1:
                    rank3.append(rank2[i])
                    i=i-1                    
                return dict(rank=rank3)                  
        except InvalidRequestError:
            return dict(id=0)  
    @expose('json')
    def warrank(self,type,off,num,uid):
        rank1=[]
        rank2=[]
        rank3=[]
        off=int(off)
        num=int(num)
        type=int(type)
        uid=int(uid)
        try:
            if type==0:
                fl=[]
                fl=DBSession.query(Rank.userid,Rank.otherid,Rank.meritrank,Rank.nobilitynum,Rank.power,Rank.won).filter(Rank.meritrank<21).filter(Rank.meritrank>0).order_by(Rank.meritrank).all()
                one=[]
                for n in fl:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
		    one=list(one)
		    one.append(n[1])
		    one.append(n[2])
		    one.append(n[4])
		    one.append(n[5])
                    one.append((int(n[3])/3))
                    one.append((int(n[3])%3))#papayaname,empirename,otherid,meritrank,power,won,nobility,subno
                    rank1.append(one)
                return dict(rank=rank1)
            else:
                fl=DBSession.query(Papayafriend.papayaid).filter_by(uid=int(uid)).all()
                fll=[]
                one=[]
                flll=[]
                rank2=[]
                for n in fl:
                    fll.append(n[0])
                otherid=DBSession.query(operationalData.otherid).filter_by(userid=int(uid)).one()#add user himself
                otherid=list(otherid)
                fll.append(otherid[0])
		rank1=DBSession.query(Rank.userid,Rank.otherid,Rank.meritrank,Rank.nobilitynum,Rank.power,Rank.won).filter(Rank.otherid.in_(fll)).order_by(Rank.meritrank).all()
                for n in rank1:
      	            one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
		    one.append(n[1])
		    one.append(n[2])
		    one.append(n[4])
		    one.append(n[5])
                    one.append((int(n[3])/3))
                    one.append((int(n[3])%3))#papayaname,empirename,otherid,meritrank,power,won,nobility,subno
                    rank2.append(one) 
                if rank2==None or len(rank2)==0:
                    return dict(id=0)
                i = off - 1
                j = off + num - 2
                if j >= len(rank2)-1:
                    j=len(rank2)-1
                while i <= j:
                    rank3.append(rank2[i])
                    i = i + 1
                return dict(rank=rank3)                  
        except InvalidRequestError:
            return dict(id=0)        
    @expose('json')
    def fortunerank(self,type,off,num,uid):
        rank1=[]
        rank2=[]
        rank3=[]
        off=int(off)
        num=int(num)
        type=int(type)
        uid=int(uid)
        try:
            if type==0:
                fl=[]
                fl=DBSession.query(Rank.userid,Rank.otherid,Rank.fortunerank,Rank.lev,Rank.corn).filter(Rank.fortunerank<21).order_by(Rank.fortunerank).all()
                one=[]
                for n in fl:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank1.append(one)
                return dict(rank=rank1)
            else:
                fl=DBSession.query(Papayafriend.papayaid).filter_by(uid=int(uid)).all()
                fll=[]
                flll=[]
                rank2=[]
                for n in fl:
                    fll.append(n[0])
                otherid=DBSession.query(operationalData.otherid).filter_by(userid=int(uid)).one()#add user himself
                otherid=list(otherid)
                fll.append(otherid[0])
                rank1=DBSession.query(Rank.userid,Rank.otherid,Rank.fortunerank,Rank.lev,Rank.corn).filter(Rank.otherid.in_(fll)).order_by(Rank.fortunerank).all()
                for n in rank1:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank2.append(one)
                if rank2==None or len(rank2)==0:
                    return dict(id=0)
                i = off - 1#the index of begin
                j = off + num - 2#the index of end
                if j >= len(rank2)-1:
                    j=len(rank2)-1
                while i <= j:
                    rank3.append(rank2[i])
                    i = i + 1
                return dict(rank=rank3)                  
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def foodrank(self,type,off,num,uid):
        rank1=[]
        rank2=[]
        rank3=[]
        off=int(off)
        num=int(num)
        type=int(type)
        uid=int(uid)
        try:
            if type==0:
                fl=[]
                fl=DBSession.query(Rank.userid,Rank.otherid,Rank.foodrank,Rank.lev,Rank.food).filter(Rank.foodrank<21).order_by(Rank.foodrank).all()
                one=[]
                for n in fl:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank1.append(one)
                return dict(rank=rank1)
            else:
                fl=DBSession.query(Papayafriend.papayaid).filter_by(uid=int(uid)).all()
                fll=[]
                flll=[]
                rank2=[]
                for n in fl:
                    fll.append(n[0])
                otherid=DBSession.query(operationalData.otherid).filter_by(userid=int(uid)).one()#add user himself
                otherid=list(otherid)
                fll.append(otherid[0])
                rank1=DBSession.query(Rank.userid,Rank.otherid,Rank.foodrank,Rank.lev,Rank.food).filter(Rank.otherid.in_(fll)).order_by(Rank.foodrank).all()
                for n in rank1:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank2.append(one)
                if rank2==None or len(rank2)==0:
                    return dict(id=0)
                i = off - 1#the index of begin
                j = off + num - 2#the index of end
                if j >= len(rank2)-1:
                    j=len(rank2)-1
                while i <= j:
                    rank3.append(rank2[i])
                    i = i + 1
                return dict(rank=rank3)
        except InvalidRequestError:
            return dict(id=0) 
    @expose('json')
    def exprank(self,type,off,num,uid):
        rank1=[]
        rank2=[]
        rank3=[]
        off=int(off)
        num=int(num)
        type=int(type)
        uid=int(uid)
        try:
            if type==0:
                fl=[]
                fl=DBSession.query(Rank.userid,Rank.otherid,Rank.exprank,Rank.lev,Rank.exp).filter(Rank.exprank<21).order_by(Rank.exprank).all()
                one=[]
                for n in fl:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank1.append(one)#papayaname,empirename,otherid,exprank,lev,exp
                return dict(rank=rank1)
            else:
                fl=DBSession.query(Papayafriend.papayaid).filter_by(uid=int(uid)).all()
                fll=[]
                flll=[]
                rank2=[]
                for n in fl:
                    fll.append(n[0])
                otherid=DBSession.query(operationalData.otherid).filter_by(userid=int(uid)).one()#add user himself
                otherid=list(otherid)
                fll.append(otherid[0])
                rank1=DBSession.query(Rank.userid,Rank.otherid,Rank.exprank,Rank.lev,Rank.exp).filter(Rank.otherid.in_(fll)).order_by(Rank.exprank).all()
                for n in rank1:
                    one=DBSession.query(operationalData.papayaname,operationalData.empirename).filter_by(userid=int(n[0])).one()
                    one=list(one)
                    one.append(n[1])
                    one.append(n[2])
                    one.append(n[3])
                    one.append(n[4])
                    rank2.append(one)
                if rank2==None or len(rank2)==0:
                    return dict(id=0)
                i = off - 1#the index of begin
                j = off + num - 2#the index of end
                if j >= len(rank2)-1:
                    j=len(rank2)-1
                while i <= j:
                    rank3.append(rank2[i])
                    i = i + 1
                return dict(rank=rank3)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def war(self,uid):#对外接口，战争结果
        print 'fetch warresult ' + str(uid)
        if uid==None:
            return dict(id=0)
        uid=int(uid)
        battleresult=warresult2(uid) 
        u=checkopdata(uid)#cache
        try:
            vic = DBSession.query(Victories).filter_by(uid=uid).one()
        except:
            print "not find victories " + str(uid)
            vic = Victories(uid, 0, 0)
            DBSession.add(vic)
        min = calev(u, vic)
        u.subno = min[0]
        nob = u.nobility*3 + u.subno
        return dict(nobility=nob,battleresult=battleresult,subno=u.subno, defence=u.defencepower, minus=min[1], corn=u.corn, cae = u.cae, inf = u.infantrypower, cav = u.cavalrypower) 
    def callost(myFull, eneFull, myPure, enePure, type):
    	lost = [0, 0]
    	attackLost = [[40, 50, 70, 90], [15, 20, 20, 20] ]
        defenceLost = [[35, 35, 35, 35], [20, 30, 45, 45] ]
        attackPow = [myFull, myPure]
        defencePow = [eneFull, enePure]
        if type == 0:
        	attackPow = [eneFull, enePure]
        	defencePow = [myFull, myPure]
        attWin = 1
        winPow = attackPow
        losePow = defencePow
        if attackPow[0] < defencePow[0]:
			attWin = 0
			winPow = defencePow
			losePow = attackPow
		        	
        situation = 0
        stage = [2, 10, 100]
        for i in stage:
        	if winPow[0] < losePow[0]*i:
        		break
        	situation += 1
        #attack power lost
        if attWin == 1:
            lost[1]=int((defencePow[1]*defenceLost[attWin][situation] + defenceLost[attWin][situation]-1)/100)#defence lost
            lost[0]=int((defencePow[1]*attackLost[attWin][situation] + attackLost[attWin][situation]-1)/100)#attack won
        else:
            lost[1]=int((attackPow[1]*defenceLost[attWin][situation] + defenceLost[attWin][situation]-1)/100)#defence lost
            lost[0]=int((attackPow[1]*attackLost[attWin][situation] + attackLost[attWin][situation]-1)/100)#attack won
        if type == 0:
        	temp = lost[0]
        	lost[0] = lost[1]
        	lost[1] = lost[0]
        print "lost is my " + str(lost[0]) + ' ene ' + str(lost[1])
        print "attack win ? " + str(attWin)
        print "attack full Power " + str(attackPow[0]) + ' att pure ' + str(attackPow[1]) + 'def full ' + str(defencePow[0]) + ' defp ' + str(defencePow[1])
        return lost     
    def getresource(kill,u,type):#type=0进攻胜利，1进攻失败，2防御胜利，3防御失败
        bonusstring=''
        k=random.randint(1,100)
        type=int(type)
        cornget = 0
        cornlost = 0
        if type==0:
            if k<=3:
                u.cae=u.cae+u.nobility+1
                bonusstring=str(u.nobility+1)+'!'
                print inspect.stack()[0]

            else:
                cornget=cornget+500*(u.nobility+1)
                u.corn=u.corn+500*(u.nobility+1)
                bonusstring='0!'
            if u.nobility<7 and u.subno<3:
                cornget += battlebonus[u.nobility][u.subno]+kill*30
                u.corn += cornget
            bonusstring=bonusstring+str(cornget)+'!'+str(cornlost)
        elif type==1:
            bonusstring='0!'
            cornget=kill*25
            u.corn += cornget
            bonusstring=bonusstring+str(cornget)+'!'+str(cornlost)
        elif type==2:
            bonusstring='0!'
            cornget=kill*20
            u.corn+=cornget
            bonusstring=bonusstring+str(cornget)+'!'+str(cornlost)  
        else:
            bonusstring='0!'
            cornlost =-int((u.corn+20-1)/20)
            cornget = kill*20
            u.corn += cornget+cornlost
            bonusstring=bonusstring+str(cornget)+'!'+str(cornlost)     
        return bonusstring 
    def calGod(uid, power):
        
        u = checkopdata(uid)
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        godTime = [3600, 21600, 86400]
        powerAdd = [2, 4, 6, 8, 10]
        assist = 0
        if u.war_god > 0 and u.war_god <= 3:
            if curTime - u.wargodtime < godTime[u.war_god-1]:
                if u.war_god_lev > 0 and u.war_god_lev <= len(powerAdd):
                    assist = int(power*powerAdd[u.war_god_lev-1]/100)
        print "god assist " + str(assist)
        return assist
    #remove readed battle
    global emptyLost
    def emptyLost(battle):
        try:
            empty = DBSession.query(EmptyCastal).filter_by(cid=-battle.enemy_id).one()
        except:
            return
        attacker = checkopdata(battle.uid)
        defencer = checkopdata(empty.uid)
        attStr = []
        defStr = []
        if empty.uid == attacker.userid:
            empty.inf += battle.powerin
            empty.cav += battle.powerca
            attStr = [0, battle.uid, -battle.enemy_id, battle.powerin, battle.powerca]
            result = EmptyResult(uid=battle.uid, data=json.dumps(attStr))
            DBSession.add(result)
            return

        attPurePow = battle.powerin + battle.powerca
        attFullPow = attPurePow
        attGod = calGod(attacker.userid, attPurePow)
        attFullPow += attGod
        attFullPow += battle.allypower
        defPurePow = empty.inf + empty.cav
        factor = 1.5 + empty.attribute*0.1
        defFullPow = int(defPurePow * factor)
        lost = callost(attFullPow, defFullPow, attPurePow, defPurePow, 1)

        returnIn = battle.powerin - lost[0]
        returnCa = battle.powerca + min(returnIn, 0)
        returnIn = max(returnIn, 0)
        returnCa = max(returnCa, 0)

        leftIn = empty.inf - lost[1]
        leftCa = empty.cav + min(leftIn, 0)
        leftIn = max(leftIn, 0)
        leftCa = max(leftCa, 0)
        
        #lose no reward
        #type 0 send uid enemy_id suc/fail attackerPower left defencePower left attackReward defeReward
        #type 1 attack     
        attStr = [1, battle.uid, -battle.enemy_id]
        if attFullPow > defFullPow:
            attStr.append(1)
        else:
            attStr.append(0)
        attStr += [battle.powerin, battle.powerca, attGod, battle.allypower, returnIn, returnCa, empty.inf, empty.cav, leftIn, leftCa]#full god ally
        
        if attFullPow > defFullPow:

            print "attack return In " + str(returnIn) + " returnca " + str(returnCa)
            empty.inf = returnIn
            empty.cav = returnCa

            curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
            if empty.uid != -1:
                proTime = (curTime - empty.lastTime)*1.0 / 3600
            empty.lastTime = curTime
            attacker.corn += EmptyLev[empty.attribute][2]
            attacker.food += EmptyLev[empty.attribute][3]
            attacker.wood += EmptyLev[empty.attribute][4]
            attacker.stone += EmptyLev[empty.attribute][5]
            if empty.uid != -1:#not monster
                coinGen = int(proTime * EmptyLev[empty.attribute][6]/2)
                foodGen = int(proTime * EmptyLev[empty.attribute][7]/2)
                woodGen = int(proTime * EmptyLev[empty.attribute][8]/2)
                stoneGen = int(proTime * EmptyLev[empty.attribute][9]/2)

                defencer.infantrypower += leftIn
                defencer.cavalrypower += leftCa
                defencer.corn += coinGen
                defencer.food += foodGen
                defencer.wood += woodGen
                defencer.stone += stoneGen
                #attack empty left Resource
                defStr = list(attStr)
                defStr += [coinGen, foodGen, woodGen, stoneGen]
            attStr += [EmptyLev[empty.attribute][2], EmptyLev[empty.attribute][3], EmptyLev[empty.attribute][4], EmptyLev[empty.attribute][5]]
            empty.uid = attacker.userid
        else:
            attacker.infantrypower += returnIn
            attacker.cavalrypower += returnCa
            empty.inf = leftIn
            empty.cav = leftCa
            defStr = attStr
        
        if attStr != []:
            result = EmptyResult(uid=attacker.userid, data=json.dumps(attStr))
            DBSession.add(result)
        if defencer != None:
            result = EmptyResult(uid=defencer.userid, data=json.dumps(defStr))
            DBSession.add(result)
    
    #update user empty battle result
    #caculate all battle result
    @expose('json')
    def emptyBattle(self, uid):
        uid = int(uid)
        user = checkopdata(uid)
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        emptySet = DBSession.query(Battle).filter("finish = 0 and (left_time+timeneed) < :curTime and enemy_id < 0").params(curTime=curTime).order_by(Battle.left_time+Battle.timeneed).all()
        print "emptyBattle", emptySet
        for b in emptySet:
            b.finish = 1
            emptyLost(b)
        emptyres = DBSession.query(EmptyResult).filter_by(uid=uid).all()#remove read in other function
        res = []
        data = []
        for e in emptyres:
            data = json.loads(e.data)
            res.append(data)
            DBSession.delete(e)#remove readed result
        try:
            userEmpty = json.loads(user.emptyResult)
        except:
            userEmpty = []
        if res != []:
            user.emptyResult = json.dumps(userEmpty+res)
        return dict(result = res)
    """
    @expose('json')
    def emptyBattle(self, uid):
        uid = int(uid)
        user = checkopdata(uid)
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        #defence my empty
        emptySet = DBSession.query(EmptyCastal.cid, Battle.uid, Battle.enemy_id).filter(Battle.enemy_id < 0).filter(Battle.uid != uid).filter(EmptyCastal.uid == uid).filter(EmptyCastal.cid == -Battle.enemy_id).filter(Battle.finish == 0).filter(Battle.timeneed+Battle.left_time < curTime).order_by(Battle.left_time).all()
        print "defence my empty ", emptySet
        for e in emptySet:
            b = DBSession.query(Battle).filter_by(uid=e[1]).filter_by(enemy_id=e[2]).one()
            b.finish = 1
            emptyLost(b)
        #attack other empty
        emptySet = DBSession.query(Battle).filter("uid = :uid and finish = 0 and enemy_id < 0 and (timeneed+left_time)<:curTime").params(uid = uid, curTime = curTime).all()
        print "attack other empty " , emptySet
        for b in emptySet:        
            b.finish = 1
            emptyLost(b)
        
        emptyres = DBSession.query(EmptyResult).filter_by(uid=uid).all()#remove read in other function
        res = []
        data = []
        for e in emptyres:
            data = json.loads(e.data)
            res.append(data)
            DBSession.delete(e)#remove readed result
        try:
            userEmpty = json.loads(user.emptyResult)
        except:
            userEmpty = []
        if res != []:
            user.emptyResult = json.dumps(userEmpty+res)
        return dict(result = res)
    """
    def warresult2(uid):
        uid = int(uid)
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        minus = -1
        battleset = []
        print 'current time ' + str(t)
        battleset = DBSession.query(Battle).filter_by(finish = 0).filter(Battle.timeneed+Battle.left_time<t).filter(or_(Battle.uid==uid, Battle.enemy_id==uid)).filter(Battle.enemy_id >= 0).order_by(Battle.left_time).all()
        print "fetch battle result of " + str(uid)
        
        #gen two battle result ord
        for b in battleset:
            print 'battle attacker ' + str(b.uid) + ' def ' + str(b.enemy_id) + ' finish ' + str(b.finish)
            if b.finish != 0:
                continue        
            attack = checkopdata(b.uid)
            defence = checkopdata(b.enemy_id)
            if attack == None or defence == None:
                continue
            attStr = str(b.enemy_id)+',1'
            defStr = str(b.uid)+',0'
            attPurePow = b.power
            attFullPow = attPurePow 
            attGod = calGod(attack.userid, attPurePow)
            attFullPow += attGod
            attFullPow += b.allypower
            print "attack full power " + str(attFullPow)

            defPurePow = defence.infantrypower + defence.cavalrypower
            defFullPow = defPurePow
            defGod = calGod(defence.userid, defPurePow)
            defFullPow += defGod
            defFullPow += defence.defencepower
            defFullPow += allyhelp(defence.userid, 1, defPurePow)
            print "defence full power " + str(defFullPow)
            
            lost = callost(attFullPow, defFullPow, attPurePow, defPurePow+defence.defencepower, 1)
            print "att Lost " + str(lost[0]) + " def lost " + str(lost[1])
            #check if in weak protect mode
            weakMode = False
            if attFullPow > defFullPow:
                defWar = defence.battleresult + ';' + defence.nbattleresult
                defWar = defWar.split(';')
                length = len(defWar)
                #fail three times
                fails = 0
                i = length - 1
                while i >= 0 and fails < 3:
                    res = defWar[i].split(',')
                    if len(res) < 2:
                        i -= 1
                        continue
                    if int(res[2]) == 1:
                        break
                    if int(res[1]) == 0:#defence fail
                        fails += 1
                    i -= 1
                if fails == 3:
                    weakMode = True
            #if in weak Mode just lost defence 5%
            if weakMode:
                print "weak mode"
                lost[1] = (defPurePow+defence.defencepower) * 5 /100
            print "def lost " + str(lost[1])
            #update power data
            returnIn = b.powerin - lost[0]
            returnCa = b.powerca + min(returnIn, 0)
            returnIn = max(returnIn, 0)
            returnCa = max(returnCa, 0)
            attLostIn = b.powerin - returnIn
            attLostCa = b.powerca - returnCa
            print "attack return In " + str(returnIn) + " returnca " + str(returnCa)
            attack.infantrypower += returnIn
            attack.cavalrypower += returnCa


            #update power data
            leftIn = defence.infantrypower - lost[1]
            leftCa = defence.cavalrypower + min(leftIn, 0)
            leftIn = max(leftIn, 0)
            leftDef = defence.defencepower + min(leftCa, 0)
            leftCa = max(leftCa, 0)
            leftDef = max(leftDef, 0)
            defLostIn = defence.infantrypower - leftIn
            defLostCa = defence.cavalrypower - leftCa
            defLostDef = defence.defencepower - leftDef
            print "defence left inf cav def " + str(leftIn) + ' ' + str(leftCa) +' ' + str(leftDef)
            defence.infantrypower = leftIn
            defence.cavalrypower = leftCa
            defence.defencepower = leftDef

            attReward = ""
            defReward = ""
            
            attVict = DBSession.query(Victories).filter_by(uid=attack.userid).one()
            defVict = DBSession.query(Victories).filter_by(uid=defence.userid).one()
            if attFullPow > defFullPow:
                print "attack win"
                attStr += ',1,'
                defStr += ',0,'

                #update victories
                attVict.won += 1
                attVict.woninmap += 1
                defVict.delostinmap += 1
                defVict.delost += 1
                print "update occupation " + str(attack.userid) + ' ' + str(defence.userid)
                #update occupation
                try:
                    print "try find if occ exist"
                    occ = DBSession.query(Occupation).filter_by(masterid=attack.userid).filter_by(slaveid=defence.userid).one()
                    print "occ value is " + str(occ.masterid) + ' slave ' + str(occ.slaveid)
                    occ.time = b.timeneed + b.left_time

                except InvalidRequestError:
                    print "insert new occ record into db"
                    occ = Occupation(attack.userid, defence.userid, b.timeneed+b.left_time)
                    DBSession.add(occ)

                addnews(attack.userid, defence.otherid, 3, t, defence.user_kind)
                addnews(defence.userid, attack.otherid, 4, t, attack.user_kind)

                attReward = getresource(lost[0], attack, 0)
                defReward = getresource(lost[1], defence, 3)
            else: 
                print "attack fail"
                attStr += ',0,'
                defStr += ',1,'

                #update victories
                attVict.lost += 1
                attVict.lostinmap += 1
                defVict.dewon += 1
                defVict.dewoninmap += 1

                attReward = getresource(lost[0], attack, 1)
                defReward = getresource(lost[1], defence, 2)

            attStr += str(lost[0])+','+str(attFullPow)+','+str(defFullPow)+','+attReward + ',' + defence.otherid+','+str(returnIn)+','+str(returnCa)+','+defence.empirename+','+str(defence.nobility*3+defence.subno)+','+str(defence.infantrypower)+','+str(defence.cavalrypower)+','+str(attGod)+','+str(defGod)+','+str(defence.defencepower)
            defStr += str(lost[1])+','+str(defFullPow)+','+str(attFullPow)+','+defReward+','+attack.otherid+','+str(defence.infantrypower)+','+str(defence.cavalrypower)+','+attack.empirename+','+str(attack.nobility*3+attack.subno)+','+str(attack.infantrypower)+','+str(attack.cavalrypower)+','+str(defGod)+','+str(attGod)+','+str(defence.defencepower)

            if attack.nbattleresult == '' or attack.nbattleresult == None:
                attack.nbattleresult = attStr
            else:
                attack.nbattleresult = attack.nbattleresult + ';' + attStr
            if defence.nbattleresult == '' or defence.nbattleresult == None:
                defence.nbattleresult = defStr
            else:
                defence.nbattleresult = defence.nbattleresult + ';' + defStr

            if attFullPow > defFullPow:
            	b.finish = 1
            else:
                b.finish = 2
        #defence fail lost 3% corn
        user = checkopdata(uid)
        if user.nbattleresult == '' or user.nbattleresult == None:
            return ''
        temp = user.nbattleresult
        DBSession.flush()
        #user.nbattleresult = ''
        return temp    
    @expose('json')
    def removeRead(self, uid, warList):#[] json array
        user = checkopdata(uid)
        battle = user.nbattleresult
        battle = battle.split(';')
        rems = json.loads(warList)
        rems = set(rems)
        left = []
        readed = []
        i = 0
        print "remove " + str(rems)
        for b in battle:
            if not i in rems:
                left.append(b)
            else:
                readed.append(b)
            i += 1
        readStr = ''
        i = 0
        for b in readed:
            if i == 0:
                readStr += b
            else:
                readStr += ';'+b
            i += 1
        if user.battleresult == '' or user.battleresult == None:
            user.battleresult = readStr
        else:
            user.battleresult += ';'+readStr

        nbat = ''
        i = 0
        for b in left:
            if i == 0:
                nbat += b
            else:
                nbat += ';'+b
            i += 1
        user.nbattleresult = nbat
        return dict(id=1, left = len(left))
    def recalev(u,v):
        nobility1=u.nobility
        base = [1, 6, 14, 29, 40, 137]
        if nobility1 < 0 or nobility1 >= len(base):
            return -1
        wonInMap = v.woninmap
        need = base[nobility1]
        if wonInMap < need:
            return need-wonInMap
        if wonInMap < 2*need:
            return need*2-wonInMap
        if wonInMap < 3*need:
            return need*3-wonInMap
        return 0#can update nobility
    def calev(u,v):#计算爵位等级，在warresult中调用
        nobility1=u.nobility
        subno=0
        minus=-1
        base = [1, 6, 14, 29, 40, 137]
        if nobility1 < 0 or nobility1 >= len(base):
            return [subno, minus]
        wonInMap = v.woninmap
        need = base[nobility1]
        if wonInMap < need:
            u.subno = 0
            return [0, need-wonInMap]
        if wonInMap < 2*need:
            u.subno = 1
            return [1, need*2-wonInMap]
        if wonInMap < 3*need:
            u.subno = 2
            return [2, need*3-wonInMap]
        u.subno = 2
        return [2, 0]#can update nobility
    @expose('json')
    def battlelist(self,uid):
        alist=[]
        dlist=[]
        attacklist=[]
        defencelist=[]
        uid=int(uid)
        alist=DBSession.query(Battle).filter_by(uid=uid).filter(Battle.enemy_id>0).order_by(desc(Battle.left_time))
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        for x in alist:
            if x.finish==0:
                ue=checkopdata(x.enemy_id)#cache
                wue=DBSession.query(warMap).filter_by(userid=x.enemy_id).one()
                
                atemp=[ue.otherid,x.timeneed+x.left_time,x.powerin,x.powerca,ue.user_kind,wue.gridid]
                attacklist.append(atemp)
        dlist=DBSession.query(Battle).filter_by(enemy_id=uid).filter(Battle.enemy_id>0).order_by(desc(Battle.left_time))
        for x in dlist:
            if x.finish==0 and t-x.left_time>0 :
                #ue=DBSession.query(operationalData).filter_by(userid=x.uid).one()
                ue=checkopdata(x.uid)#cache
                wue=DBSession.query(warMap).filter_by(userid=x.uid).one()                
                if ue == None or wue == None:
                    continue
                dtemp=[ue.otherid,x.timeneed+x.left_time,x.powerin,x.powerca,ue.user_kind,wue.gridid]
                defencelist.append(dtemp)    
        mapEmpBat = mapEmptyBattle(uid)
        return dict(attacklist=attacklist,defencelist=defencelist, emptyAtt = mapEmpBat['emptyAtt'], emptyDef = mapEmpBat['emptyDef'])
    
    @expose('json')
    def warrecord(self,uid):#对外接口，战绩
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
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
    global calProtect
    def calProtect(kind, time):
        ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
        proTime = [7200, 28800, 86400]
        if kind == -1:
            return -1
        else:
            if kind >= 0 and kind < len(proTime):
                if ti - time > proTime[proType]:
                    return -1
                return proTime[proType] + time
        return -1

    #empty City Position
    #@expose('json')
    global mapEmptyInfo
    def mapEmptyInfo(uid, mid):
        mid = int(mid)
        empty = DBSession.query(EmptyCastal.cid, EmptyCastal.uid, EmptyCastal.gid, EmptyCastal.inf, EmptyCastal.cav, EmptyCastal.attribute, EmptyCastal.lastTime).filter("mid = :mid ").params(mid=mid).all()
        return dict(empty = empty)
    @expose('json')
    def userHisEmptyWar(self, uid):
        uid = int(uid)
        user = checkopdata(uid)
        return user.emptyResult
    #occupation Data
    @expose('json')
    def mapOccData(self, uid):
        uid = int(uid)
        occData = DBSession.query(Occupation.slaveid).filter_by(masterid = uid).all()
        return dict(occData = occData)
    #fighting emptyWar
    #@expose('json')
    global mapEmptyBattle
    def mapEmptyBattle(uid):
        uid = int(uid)
        myAttack = DBSession.query(operationalData.otherid, -Battle.enemy_id, Battle.left_time+Battle.timeneed, Battle.powerin, Battle.powerca, Battle.allypower).filter(operationalData.userid == Battle.uid).filter(Battle.uid==uid).filter(Battle.enemy_id < 0).filter(Battle.finish == 0).all()
        #from_statement("select uid, enemy_id, left_time, timeneed, powerin, powerca, allypower from battle where uid=:uid and enemy_id < 0 and finish = 0").params(uid=uid).all()
        myDef = DBSession.query(operationalData.otherid, EmptyCastal.cid, Battle.left_time+Battle.timeneed, Battle.powerin, Battle.powerca, Battle.allypower).filter_by(userid=Battle.uid).filter(EmptyCastal.uid == uid).filter(EmptyCastal.cid == -Battle.enemy_id).filter_by(finish = 0).all()
        #.from_statement("select battle.uid, enemy_id, left_time, timeneed, powerin, powerca, allypower from battle, emptyCastal where emptyCastal.uid = :uid and enemy_id = -cid and finish = 0").params(uid=uid).all()
        return dict(emptyAtt = myAttack, emptyDef = myDef)
    """
    #userinformation  battle mapinformation
    @expose('json')
    def warinfo(self, userid):#map information
        uid = int(userid)
        user = checkopdata(uid)
        curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
        if user.nobility < 0:
            user.protecttype = 2
            user.protecttime = curTime
            mapgrid = moveMap(user.userid)
            user.nobility = 0
        vict = DBSession.query(Victories).filter_by(uid=uid).one()
        warmap = DBSession.query(warMap).filter_by(userid=uid).one()
        allCity = DBSession.query(operationalData, warMap).from_statement("select otherid, user_kind, nobility, gridid, empirename, userid, subno, protecttype, protecttime from operationalData, warMap where operationalData.userid = warMap.userid and mapid = :mapid").params(mapid=warmap.mapid).all()#fetch all city

        #return initial data of city and occupation data
        for a in allCity:
            a[7] = calProtect(a[7], a[8])
            try:
                occData.index(a[5])
                a[8] = 1
            except:
                a[8] = 0
        sub = recalev(user, vict)    
        if u.warcurrenttask=='' or u.warcurrenttask==None or u.warcurrenttask=='-1' or int(u.warcurrenttask)<0:
            wwartask=-1
        else:
            wwartask=wartaskbonus[int(u.warcurrenttask)][0]              
        attList = DBSession.query(Battle).from_statement("select enemy_id, left_time, timeneed, powerin, powerca from battle where battle.uid = :uid and finish = 0 and battle.enemy_id > 0 order by left_time").params(uid=uid).all() 
        defList = DBSession.query(Battle).from_statement("select uid, left_time, timeneed, powerin, powerca from battle where battle.enemy_id = :uid and finish = 0 order by left_time").params(uid=uid).all()
        userProtect = checkprotect(user)

        return dict(sub=sub,wartask=wwartask,protect=userprotect,mapid=warmap.mapid,newstr=user.signtime,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,citydefence=user.defencepower,attacklist=attList,defencelist=defList,time=curTime,gridid=warmap.gridid,monsterstr=user.monsterlist,nobility=user.nobility,subno=user.subno,won=vict.won,lost=vict.lost,list=allCity)
    """
    @expose('json')
    def warinfo(self,userid):#对外接口，战报
        userid=int(userid)
        v=None
        m=None
        u1=None
        bili=0
        attacklist=[]
        defencelist=[]
        u1=None
        l1=[]
        list1=[]
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        mapgrid=None
        wartask=None
        userprotect=-1
        u=checkopdata(userid)#cache
            
        try:

            if u.nobility<0:
                u.protecttype = 2
                u.protecttime = t
                mapgrid = moveMap(u.userid)
                u.nobility = 0
            v=DBSession.query(Victories).filter_by(uid=userid).one()
            m=DBSession.query(warMap).filter_by(userid=userid).one()
            
            newstr=u.signtime
            nobility1=u.nobility
            subno=u.subno
            won=v.won
            lost=v.lost
            list1=DBSession.query(warMap).filter_by(mapid=m.mapid)
            listuser=[]
            alist=DBSession.query(Battle).filter_by(uid=userid)
            if u.warcurrenttask=='' or u.warcurrenttask==None or u.warcurrenttask=='-1' or int(u.warcurrenttask)<0:
                wwartask=-1
            else:
                wwartask=wartaskbonus[int(u.warcurrenttask)][0]              
            for x in alist:
                if x.finish==0:
                    #ue=DBSession.query(operationalData).filter_by(userid=x.enemy_id).one()
                    ue=checkopdata(x.enemy_id)#cache
                    wue=DBSession.query(warMap).filter_by(userid=x.enemy_id).one()
                    atemp=[ue.otherid,x.timeneed+x.left_time,x.powerin,x.powerca,ue.user_kind,wue.gridid]
                    attacklist.append(atemp)
            dlist=DBSession.query(Battle).filter_by(enemy_id=userid)
            for x in dlist:
                if x.finish==0 :
                    #ue=DBSession.query(operationalData).filter_by(userid=x.uid).one()
                    try:
                    	ue=checkopdata(x.uid)#cache
                    	wue=DBSession.query(warMap).filter_by(userid=x.enemy_id).one()
                    	dtemp=[ue.otherid,x.timeneed+x.left_time,x.powerin,x.powerca,ue.user_kind,wue.gridid]
                    	defencelist.append(dtemp)
                    except:
                        print "user deleted"
            for l in list1 :
                l1=[]
                try:
                    #u1=DBSession.query(operationalData).filter_by(userid=l.userid).one()
                    u1=checkopdata(l.userid)#cache
                    l1.append(u1.otherid)
                    l1.append(u1.user_kind)
                    l1.append(u1.nobility)
                    l1.append(l.gridid)
                    l1.append(u1.empirename)
                    l1.append(u1.userid)
                    l1.append(u1.subno)
                    l1protect=checkprotect(u1)
                    l1.append(l1protect)                    
                    #newstr=u1.signtime
                    #l1.append(newstr)
                    try:
                        occ=DBSession.query(Occupation).filter_by(masterid=userid).filter_by(slaveid=l.userid).one()
                        l1.append(1)
                    except InvalidRequestError:
                        l1.append(0)

                    if l.userid != userid:
                        listuser.append(l1)
                        
                except: 
                    continue               
            #ca=calev(u,v)
            sub=0
            sub=recalev(u,v)
            userprotect=checkprotect(u)
            #mapEmpty = mapEmptyBattle(userid) 
            emptyInfo = mapEmptyInfo(userid, m.mapid)
            return dict(empty = emptyInfo['empty'], sub=sub,wartask=wwartask,protect=userprotect,mapid=m.mapid,newstr=newstr,infantrypower=u.infantrypower,cavalrypower=u.cavalrypower,citydefence=u.defencepower,attacklist=attacklist,defencelist=defencelist,time=t,gridid=m.gridid,monsterstr=u.monsterlist,nobility=nobility1,subno=subno,won=won,lost=lost,list=listuser)
        except InvalidRequestError:
            return dict(u=u.userid,v=v.uid,map=mapgrid)
    # city:a,b;c,d 
    # no check
    @expose('json')
    def move(self, movestring):
        print "move " + movestring
        strs = movestring.split(':')
        city = int(strs[0])

        strs = strs[1].split(';')
        src = []
        tar = []
        for s in strs:
            s = s.split(',')
            src.append(int(s[0]))
            tar.append(int(s[1]))
        src2 = set(src)
        tar2 = set(tar)
        if len(src) != len(src2):
            print "src repeat"
            return dict(id=0, reason="src repeat")
        if len(tar) != len(tar2):
            print "tar repeat"
            return dict(id=0, reason="tar repeat")
        allbuilding = DBSession.query(businessWrite.grid_id).filter(businessWrite.city_id==city).filter(businessWrite.ground_id != -1).all()
        temp = []
        for b in allbuilding:
            temp.append(b[0])
        allbuilding = set(temp)
        dif = allbuilding - src2
        remainLen = len(allbuilding) - len(src2)
        difLen = len(dif)
        #print allbuilding
        #print src2
        #print dif
        if difLen != remainLen:
            print "src not exist in all"
            return dict(id=0, reason = "src not exist")
        uni = dif & tar2
        if len(uni) != 0:
            print "tar union with other"
            return dict(id=0, reason="tar union with others")
        allSrc = []#bid
        for s in src:
            building = DBSession.query(businessWrite.bid).filter_by(city_id=city).filter_by(grid_id = s).all()
            if len(building) > 0:
                allSrc.append(building[0][0])
        #move by bid
        i = 0
        DBSession.begin_nested()
        for s in src:
            t = tar[i]
            #print "move "+str(s) + 'to ' + str(t)
            building = DBSession.query(businessWrite).filter_by(city_id=city).filter_by(bid=allSrc[i]).one()
            building.grid_id = t
            i += 1
        DBSession.flush()
        return dict(id=1, result="move suc")
    @expose('json')
    def godbless(self,uid,godtype,caetype):#对外接口，施加神迹
        uid=int(uid)
        u=checkopdata(uid)#cache
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        godtype=int(godtype)
        caetype=int(caetype)
        caeCost = [3, 15, 30]
        mark=0
        warmap = DBSession.query(warMap).filter_by(userid = uid).one()
        if godtype == 4: #friendGod
            if caetype >= 0 and caetype < len(caeCost):
                buildings = DBSession.query(businessWrite).filter("businessWrite.city_id=:cid and ground_id >= 420 and ground_id <= 424 and finish = 1").params(cid=warmap.city_id).all()
                #buildings = list(buildings)
                print "friend god help now " + str(caetype)
                #print buildings
                if len(buildings) > 0:
                   if u.cae >= caeCost[caetype]:
                        u.cae -= caeCost[caetype]
                        print inspect.stack()[0]

                        b = buildings[0]
                        b.producttime = t
                        b.object_id = caetype
                        print "friend god bless suc"
                        return dict(id=1, result = "friend god bless "+ str(caetype))
            return dict(id=0, reason="cae not enough or no god") 

        print inspect.stack()[0]
        if caetype==0:
            if u.cae-3>=0:
                u.cae=u.cae-3
                if godtype==0:
                    u.food_god=1
                    u.foodgodtime=t                    
                elif godtype==1:
                    u.person_god=1
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=1
                    u.wealthgodtime=t
                else:
                    u.war_god=1
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        elif caetype==1:
            if u.cae-15>=0:
                u.cae=u.cae-15
                print inspect.stack()[0]
                if godtype==0:
                    u.food_god=2
                    u.foodgodtime=t                
                elif godtype==1:
                    u.person_god=2
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=2
                    u.wealthgodtime=t
                else:
                    u.war_god=2
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)  
        else:
            if u.cae-30>=0:
                u.cae=u.cae-30
                print inspect.stack()[0]
                if godtype==0:
                    u.food_god=3
                    u.foodgodtime=t                

                elif godtype==1:
                    u.person_god=3
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=3
                    u.wealthgodtime=t
                else:
                    u.war_god=3
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
                             
                 

    @expose('json')
    def updatebuilding(self,user_id,city_id,ground_id,grid_id,type):# 对外接口，升级建筑物update building operationalData:query->update; businessWrite:query->update
        ground_id=int(ground_id)
        try:
            ca=0
            cae=0
            price=0
            pricefood=0
            pop=0
            ground_id=int(ground_id)
            stone=0
            wood=0

            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))

            if ground_id >= 420 and ground_id <= 424:
                lev = ground_id - 420#next level
                if (p.ground_id+1) != ground_id:
                    return dict(id = 0, reason = "not friend god or lev > tar")
                #0 time 1 food 2 corn 3 exp 4 population 5 cae
                if lev <= 4:
                    if int(type) == 0:
                        if u.cae >= friendGod[lev][5]:
                            u.cae -= friendGod[lev][5]
                            print inspect.stack()[0]

                            u.populationupbound += friendGod[lev][4]
                            u.exp += friendGod[lev][3]
                            p.ground_id += 1
                            p.finish = 0
                            p.producttime = ti 
                            return dict(id=1, result="update by cae", caeCost = friendGod[lev][5])
                    else:
                        if u.food >= friendGod[lev][1] and u.corn >= friendGod[lev][2]:
                            u.food -= friendGod[lev][1]
                            u.corn -= friendGod[lev][2]
                            u.exp += friendGod[lev][3]
                            u.populationupbound += friendGod[lev][4]
                            p.ground_id += 1
                            p.finish = 0
                            p.producttime = ti
                            return dict(id=1, result="update by food")
                return dict(id=0, reason="lev or resource not correct")

            lis=getGround_id(int(ground_id))
            if lis==None:
                return dict(id=-int(ground_id))
            price=lis[0]
            if p.ground_id<=0 or p.grid_id<=0:
                return dict(id=0)
            if int(type)==0:
                if ground_id>=100 and ground_id<=199:
                    cae=lis[3]
                elif ground_id>=200 and ground_id<=299:
                    cae=lis[4]
                    pop=lis[2]
                elif ground_id>=300 and ground_id<=399:
                    cae=lis[4]
                    pop=lis[2]
                elif ground_id>=400 and ground_id<420:
                    cae=lis[2]
                    
                if u.cae-cae>=0 and u.labor_num+pop<=u.population:
                    p.producttime=ti
                    p.finish=0
                    p.ground_id=ground_id
                    p.object_id=-1
                    if u.cae-cae<u.cae:
                        u.cae=u.cae-cae
                        print inspect.stack()[0]
                    u.labor_num=u.labor_num+pop
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif p.ground_id>=100 and p.ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif p.ground_id >=200 and p.ground_id<=299:
                        u.exp=u.exp+lis[5]
                    elif p.ground_id>=300 and p.ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif p.ground_id>=400 and p.ground_id<420:
                        u.exp=u.exp+lis[3]
                        
                    if ground_id>=400 and ground_id<=499:
                        if (ground_id-400)%4==0:
                            u.foodgodtime=-1
                            u.food_god=0
                        elif (ground_id-400)%4==1:
                            u.person_god=0
                            u.popgodtime=-1
                        elif (ground_id-400)%4==2:
                            u.wealth_god=0
                            u.wealthgodtime=-1
                        elif (ground_id-400)%4==3:
                            u.war_god=0
                            u.wargodtime=-1
                        u.populationupbound=u.populationupbound+lis[4]
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                if ground_id>=1 and ground_id<=499:
                    pricefood=lis[1]
                if ground_id >=1 and ground_id<=99:
                    pop=lis[2]
                elif ground_id>=200 and ground_id<399:
                    pop=lis[2]
                if ground_id>=1 and ground_id<=99:
                    wood=lis[3]
                elif ground_id>=100 and ground_id<=199:
                    if lis[2]>0:
                        wood=lis[2]
                    else:
                        stone=-lis[2]
                elif ground_id>=200 and ground_id<=299:
                    if lis[3]>0:
                        wood=lis[3]
                    else:
                        stone=-lis[3]
                elif ground_id>=300 and ground_id<=399:
                    if lis[3]>0:
                        wood=lis[3]
                    else:
                        stone=-lis[3]
                elif ground_id>=400 and ground_id<=499:
                    pricefood=lis[1]
                if price>=0:
                    if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0  and specialgoods(int(ground_id),u.specialgoods,u)==True:
                        u.corn=u.corn-price
                        u.stone=u.stone-stone
                        u.wood=u.wood-wood
                        u.food=u.food-pricefood
                        u.labor_num=u.labor_num+pop
                        p.finish=0
                        p.producttime=ti
                        p.ground_id=int(ground_id)
                        if p.ground_id>=1 and p.ground_id<=99:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id>=100 and p.ground_id<=199:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id >=200 and p.ground_id<=299:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=300 and p.ground_id<=399:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=400 and p.ground_id<=499:
                            u.exp=u.exp+lis[3]                        
                        if int(ground_id)>=400 and int(ground_id)<=499:
                            ground_id=int(ground_id)
                            if (ground_id-400)%4==0:
                                u.foodgodtime=-1
                                u.food_god=0
                            elif (ground_id-400)%4==1:
                                u.person_god=0
                                u.popgodtime=-1
                            elif (ground_id-400)%4==2:
                                u.wealth_god=0
                                u.wealthgodtime=-1
                            elif (ground_id-400)%4==3:
                                u.war_god=0
                                u.wargodtime=-1
                            u.populationupbound=u.populationupbound+lis[4]
                        return dict(id=1)
                    else:
                        return dict(id=0,lis=lis,price=u.corn-price,food=u.food-pricefood,pop=u.labor_num+pop,s=specialgoods(int(ground_id),u.specialgoods,u),st=u.stone-stone)
                else:
                    if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and   specialgoods(int(ground_id),u.specialgoods,u)==True:
                        if u.cae+price<u.cae:
                            u.cae=u.cae+price
                            print inspect.stack()[0]
                        u.food=u.food-pricefood
                        u.labor_num=u.labor_num+pop
                        u.wood=u.wood-wood
                        u.stone=u.stone-stone
                        p.finish=0
                        p.producttime=ti
                        if p.ground_id>=1 and p.ground_id<=99:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id>=100 and p.ground_id<=199:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id >=200 and p.ground_id<=299:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=300 and p.ground_id<=399:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=400 and p.ground_id<=499:
                            u.exp=u.exp+lis[3]                        
                        #p.producttime=ti
                        p.ground_id=int(ground_id)
                        ground_id=int(ground_id)
                        if int(ground_id)>=400 and int(ground_id)<=499:
                            if (ground_id-400)%4==0:
                                u.foodgodtime=-1
                                u.food_god=0
                            elif (ground_id-400)%4==1:
                                u.person_god=0
                                u.popgodtime=-1
                            elif (ground_id-400)%4==2:
                                u.wealth_god=0
                                u.wealthgodtime=-1
                            elif (ground_id-400)%4==3:
                                u.war_god=0
                                u.wargodtime=-1      
                            u.populationupbound=u.populationupbound+lis[4]
                        return dict(id=1)
                    else:
                        return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    #hour food corn exp popupbound upgrade_cae 
    global friendGod
    global friGodReward
    friendGod = [[2*3600, 500, 10000, 50, 250, 0], [6*3600, 1000, 20000, 100, 250, 5], [12*3600, 2000, 50000, 170, 250, 10], [18*3600, 5000, 100000, 250, 250, 15], [24*3600, 10000, 500000, 350, 250, 30]]
    friGodReward = [5, 10, 20, 30, 50]
    global initH
    global addHealth
    global growUp
    global reward
    global eggCost
    eggCost = [[50000, 100, 5], [100000, 250, 6], [500000, 1000, 10], [-10, 300, 7], [-50, 1200, 12], [-100, 1500, 17]]
    initH = [0, 25, 40, 600]
    addHealth = [3, 5, 7, 7]
    growUp = [51, 100, 250, 99999999]
    reward = [[4500, 30], [9000, 40], [15000, 100], [0, 0]]

    @expose('json')
    def getBids(self, uid, cid):
        buildings = DBSession.query(businessWrite.bid, businessWrite.grid_id).filter_by(city_id = cid).all()
        return dict(id=1, bids = buildings)
    @expose('json')
    def changeStyle(self, uid, pid, style):
        dragon = DBSession.query(Dragon).filter_by(pid=pid).one()
        dragon.style = style
        return dict(id=1)
    @expose('json')
    def getPets(self, uid, cid):
        dragon = DBSession.query(Dragon.pid, Dragon.bid, businessWrite.grid_id, Dragon.state, Dragon.kind, Dragon.health, Dragon.friNum, Dragon.friList, Dragon.name, Dragon.attack, Dragon.lastFeed, Dragon.style).filter(and_(Dragon.uid == uid, businessWrite.bid==Dragon.bid)).all()#index bid
        allPets = []
        for d in dragon:
            ld = list(d)
            try:
                attribute = DBSession.query(PetAtt.att).filter_by(pid=d[0]).one()
            except:
                attribute = PetAtt(pid=d.pid, att=0)
                DBSession.add(attribute)
            ld.append(attribute.att)
            allPets.append(ld)
        return dict(id=1, pets=allPets)
    #命名宠物 修改名字
    @expose('json')#state = 2
    def namePet(self, uid, gid, name, cid):
        building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
        dragon = DBSession.query(Dragon).filter(Dragon.bid == building.bid).one()#index bid
        dragon.name = name        
        return dict(id=1)
    @expose('json')
    def changeAttr(self, uid, pid, attr):#find if exist then visit petAtt table
        print "changeAttr " + str(uid) + ' ' + str(pid) + ' ' + str(attr)
        uid = int(uid)
        pid = int(pid)
        attr = int(attr)
        pet = DBSession.query(Dragon).filter_by(pid = pid).one()
        user = DBSession.query(operationalData).filter_by(userid = uid).one()
        if pet.uid != uid:
            return dict(id=0, reason="not your pet")
        #0 solid 1 fire 2 ice
        if attr < 0:
            return dict(id=0, reason='attr not  > 0')
        if attr == 0:
            petAtt = DBSession.query(PetAtt).filter_by(pid = pid).all()
            if len(petAtt) == 0:
                petAtt = PetAtt(pid=pid, att = attr)
                DBSession.add(petAtt)
            else:
                petAtt[0].att = attr
            return dict(id=1, result="return to soil dragon")
        if user.cae >= 20:
            user.cae -= 20
            petAtt = DBSession.query(PetAtt).filter_by(pid = pid).all()
            if len(petAtt) == 0:
                petAtt = PetAtt(pid=pid, att = attr)
                DBSession.add(petAtt)
            else:
                petAtt[0].att = attr
            return dict(id=1, result='change attr suc')
        return dict(id=0, reason='cae not enough')
    #喂养宠物 self feed friend feed 
    @expose('json')
    def changeKind(self, uid, pid, kind):
        print 'changeKind ' +' ' +str(uid) +' ' +str(pid) + ' ' +str(kind)
        uid = int(uid)
        pid = int(pid)
        kind = int(kind)
        pet = DBSession.query(Dragon).filter_by(pid = pid).one()
        user = DBSession.query(operationalData).filter_by(userid = uid).one()
        if pet.uid != uid:
            return dict(id=0, reason="not your pet")
        if pet.state == 2:#0 not active 1 not buy 2
            print "is egg " + str(kind)
            if kind >= 0 and kind < len(eggCost):
                print "kind right"
                cost = eggCost[kind]
                if cost[0] > 0:#money
                    print "cost " + str(cost[0]) + ' ' + str(cost[1])
                    if user.corn >= cost[0] and user.food >= cost[1]:
                        user.corn -= cost[0]
                        pet.kind = kind
                        return dict(id=1, result="change by corn")
                else:
                    print "cost " + str(cost[0]) + ' ' + str(cost[1])
                    caeCost = abs(cost[0])
                    if user.cae >= caeCost:
                        user.cae -= caeCost
                        pet.kind = kind
                        return dict(id=1, result="change by cae")
        return dict(id=0, reason="resource not enough, not egg, kind not right")
    global needHealth 
    needHealth = [51, 201, 9999, 99999, 999999]
    @expose('json')#upgrade state
    def getUp(self, uid, pid):
        uid = int(uid)
        pid = int(pid)
        dragon = DBSession.query(Dragon).filter(Dragon.pid == pid).one()
        if dragon.uid != uid:
            return dict(id=0, reason="not your dragon")
        state = dragon.state - 2
        if state < 0 or state >= len(needHealth):
            return dict(id=0, reason="not in right state")
        if dragon.health >= needHealth[state]:
            user = checkopdata(uid)
            user.corn += reward[state][0]
            user.exp += reward[state][1]
            dragon.state += 1
            return dict(id=1, result="new state " + str(state+2))
        return dict(id=0, reason="health not enough " + str(dragon.health))
            
    @expose('json')
    def trainDragon(self, uid, gid, cid):
        uid = int(uid)
        try:
            building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
            dragon = DBSession.query(Dragon).filter(Dragon.bid == building.bid).one()
        except InvalidRequestError:
            return dict(id=0, reason="no such dragon")
        if dragon.state < 2:
            return dict(id=0, reason="not buy egg yet")
        if dragon.uid == uid:#train himself dragon
            trainNum = dragon.trainNum
            print "train dragon "+str(trainNum)
            if trainNum < 100:
                dragon.trainNum += 1
                dragon.attack +=1
                return dict(id=1, result="train dragon suc")
            else: 
                return dict(id=0,reason="trainNum>100")
        else:
            return dict(id=0,reason="not himself dragon")
    @expose('json')#state = 2  1clear all state > 2 friList = "[]" 2all health -=  3clear all feed state
    def feed(self, uid, gid, cid):
        uid = int(uid)
        try:
            building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
            dragon = DBSession.query(Dragon).filter(Dragon.bid == building.bid).one()
        except InvalidRequestError:
            return dict(id=0, reason="no such dragon")
        if dragon.state < 2:
            return dict(id=0, reason="not buy egg yet")

        state = dragon.state - 2
        if dragon.uid == uid:#feed my dragon
            #I feed 1 fri 2 not 0
            if dragon.lastFeed & 1 == 1:
                return dict(id=0, reason="you feed yet") 
            needFood = addHealth[state]*20;
            user = checkopdata(uid)
            if user.food < needFood:
                return dict(id=0, reason="food not enough")
            user.food -= needFood;
            dragon.lastFeed |= 1
            #update health
            if dragon.health <= needHealth[state]:        
                dragon.health += addHealth[state]
            return dict(id=1, result="self feed suc", state= dragon.state)
        else:
            friList = dragon.friList
            friList = json.loads(friList)
            if dragon.state >= 4:
                allowFriend = 7
            elif dragon.state == 3:
                allowFriend = 5
            else:
                allowFriend = 3
            if len(friList) > allowFriend:
                print "friend help enough"
                return dict(id = 0, reason = "enough friend helped")
            #be helped
            user = DBSession.query(warMap.userid).filter_by(city_id=cid).one()
            user = DBSession.query(operationalData).filter_by(userid = user.userid).one()
            #help
            friend = checkopdata(uid)
            uotherid = int(friend.otherid)
            try:
                pos = friList.index(uotherid)
                print "help yet " + str(uotherid) + ' ' + str(dragon.pid)
                return dict(id=0, reason="help yet")
            except:
                needFood = 20;
                if friend.food < needFood:
                    print "need more food"
                    return dict(id=0, reason="food not enough")
                friend.food -= needFood
                friend.corn += 1000
                friList.append(uotherid)
                dragon.friList = json.dumps(friList)#clear at 0:00 when friend logsign
                dragon.lastFeed |= 2
                #update health
                if dragon.health <= needHealth[state]:        
                    dragon.health += 1
                curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
                #help pet
                addnews(friend.userid, user.otherid, 6, curTime, user.user_kind)#some one help you
                return dict(id=1, result="help suc", state = dragon.state)
        print "feed fail"
        return dict(id=0, reason="unknow reason")

    #使用银币购买宠物蛋 state = 1
    @expose('json')
    def buyEgg(self, uid, cid, gid, kind):
        try:
            building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
            dragon = DBSession.query(Dragon).filter(and_(Dragon.uid == uid, Dragon.bid == building.bid)).one()
            if dragon.state != 1:
                return dict(id=0, reason = "dragon not in buy state")
            kind = int(kind)
            if kind >=0 and kind < len(eggCost):
                user = DBSession.query(operationalData).filter_by(userid = int(uid)).one()
                #print str(user.corn) + ' corn id ' + str(user.userid)
                if eggCost[kind][0] > 0:
                    if user.corn >= eggCost[kind][0]:
                        user.corn -= eggCost[kind][0]
                        user.exp += 30
                        dragon.kind = kind
                        dragon.state = 2
                        dragon.health = 9
                        dragon.attack = 0
                        dragon.name = '我的宠物'
                        return dict(id=1, result = "buy suc corn")
                    return dict(id=0, reason="need corn")
                else:
                    if user.cae >= abs(eggCost[kind][0]):
                        user.cae += eggCost[kind][0]#neg for caesar
                        user.exp += 30
                        dragon.kind = kind
                        dragon.state = 2
                        dragon.health = 9
                        dragon.attack = 0
                        dragon.name = '我的宠物'
                        return dict(id=1, result = "buy suc cae")
                    return dict(id=0, reason="need cae")
            return dict(id=0, reason="kind out of range")
        except InvalidRequestError:
            return dict(id=0, reason = "no dragon")
    global needFri
    needFri = 10#total need
    #用户宠物激活完成
    @expose('json')
    def activateComplete(self, uid, gid, cid):
        building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
        dragon = DBSession.query(Dragon).filter(and_(Dragon.uid == uid, Dragon.bid == building.bid)).one()
        if dragon.friNum >= needFri and dragon.state == 0:
            dragon.state = 1
            dragon.friList = "[]"#clear friendList
            return dict(id=1, result="active suc")
        return dict(id=0, reason="frinum not enough or state != 0")
    #帮助好友， 使用凯撒币激活宠物 进入finish状态 state = 0
    @expose('json')
    def activeDragon(self, uid, fid, gid, cid):#fid = -1 use cea others ask friend
        #select from ope
        caeCost = 1#each cost
        uid = int(uid)
        user = checkopdata(uid)

        try:
            fid = int(fid)
        except:
            print "otherid not number"

        if fid == -1:#help by cae
            print "use cae"
            try:
                building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
                dragon = DBSession.query(Dragon).filter(and_(Dragon.uid == uid, Dragon.bid == building.bid)).one()
            except InvalidRequestError:
                print str(uid) + 'not dragon ' + str(cid) + ' ' + str(gid) 
                return dict(id=0, reason="no dragon")
            if dragon.state == 0:#not active 
                if dragon.friNum >= needFri:
                    return dict(id=0, reason="friend enough", leftNum = 0)
                if user.cae >= caeCost:
                    user.cae -= caeCost
                    friList = dragon.friList
                    if friList == None:
                        friList = [-1]
                    else:
                        friList = json.loads(friList)
                        friList.append(-1)
                    dragon.friList = json.dumps(friList)
                    dragon.friNum += 1
                    return dict(id=1, leftNum = needFri - dragon.friNum)
                return dict(id=0, reason="cae not enou")
            else:
                return dict(id=0, reason="active yet")
        else:#help by others check if help yet ?
            print "I help my friend"
            #friend id other id ?
            try:
                friend = DBSession.query(operationalData).filter_by(otherid=fid).one()
                building = DBSession.query(businessWrite).filter_by(city_id=cid).filter_by(grid_id=gid).one()
                dragon = DBSession.query(Dragon).filter(and_(Dragon.uid == friend.userid, Dragon.bid == building.bid)).one()
            except InvalidRequestError:
                return dict(id = 0, reason = "no dragon here")
            if dragon.state == 0:#not active
                if dragon.friNum >= needFri:
                    return dict(id=0, reason="friend enough", leftNum = 0)
                friList = dragon.friList
                if friList == None:
                    friList = [fid]
                else:
                    friList = json.loads(friList)
                    uotherid = int(user.otherid)
                    try:
                       myPos = friList.index(uotherid)
                       return dict(id=0, reason = "you help yet")
                    except:
                        friList.append(uotherid)
                user.corn += 1000
                dragon.friList = json.dumps(friList)
                dragon.friNum += 1
                return dict(id=1, leftNum=needFri-dragon.friNum)
            else:
                return dict(id=0, reason="active yet")
        return dict(id=0, reason = "unknown reason")
    
    @expose('json')
    #return id = 1 suc  id = 0 fail 
    def build(self,user_id,city_id,ground_id,grid_id):# 对外接口，建造建筑物build operationalData:query->update; businessWrite:query->update
        print "build " + str(ground_id)
        curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
        user_id = int(user_id)
        user = checkopdata(user_id)
        #420 421 422 423 424 can't build high level
        #when visit friend add corn more
        ground_id = int(ground_id)
        if ground_id >= 420 and ground_id <= 424:
            buildings = DBSession.query(businessWrite).filter("city_id=:cid and ground_id >= 420 and  ground_id <= 424").params(cid=city_id).all();
            #print buildings
            if len(buildings) != 0:
                return dict(id=0, reason="friend god exist in city")
            buildings = DBSession.query(businessWrite).filter_by(city_id=city_id).filter_by(grid_id = grid_id).all()
            for b in buildings:
                if b.ground_id != -1:
                    return dict(id = 0, reason="building exist here")
                DBSession.delete(b)
            lev = int(ground_id)-420
            #check demands
            if lev == 0:
                if user.lev < 25:
                    return dict(id=0, reason="level < 25")
            if user.food >= friendGod[lev][1] and user.corn >= friendGod[lev][2]:
                user.food -= friendGod[lev][1]
                user.corn -= friendGod[lev][2]
                user.populationupbound += friendGod[lev][4]
                user.exp += friendGod[lev][3]

                building = businessWrite(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
                DBSession.add(building)
                read(city_id)
                return dict(id=1, result="friendgod suc")
            else:
                return dict(id=0, reason="resource not enough")
            return dict(id=0, reason="unknown")


        demands = [15, 1000, 100000]#lev 10 food 10000 corn 10W
        #upbound + 100
        if ground_id / 1000 != 0:
            print "build dragon " + str(user_id)
            coinCost = 0
            foodCost = 0
            
            #level OK
            #check Cost
            if ground_id == 1000:
                if user.lev >= demands[0] and user.food >= demands[1] and user.corn >= demands[2]:
                    print "check dragon"
                    #remove exist ground = -1 building
                    existDragon = DBSession.query(businessWrite).filter_by(city_id=city_id).filter_by(ground_id=ground_id).all()
                    if len(existDragon) != 0:
                        return dict(id=0, reason="dragon exist")
                    building = DBSession.query(businessWrite).filter_by(city_id=city_id).filter_by(grid_id=grid_id).all()
                    for b in building:
                        if b.ground_id != -1:
                            return dict(id = 0, reason = "exist building")
                        else:
                            DBSession.delete(b)

                    #not exist or exist mutiple 
                    building = businessWrite(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = 0, finish = 1)
                    DBSession.add(building)
                    building = DBSession.query(businessWrite).filter_by(city_id=city_id).filter_by(grid_id=grid_id).one()
                    
                    user.food -= demands[1]
                    user.corn -= demands[2]
                    #reward
                    user.populationupbound += 100

                    dragon = Dragon(uid = user_id, bid = building.bid, friNum = 0, state=0,  health = 0, name = '我的宠物', kind = 0, friList= '[]', lastFeed = 0, attack=0, trainNum = 0)
                    DBSession.add(dragon)
                    #update business read for logsign
                    read(city_id)
                    return dict(id=1, result = "build dragon suc")
            return dict(id = 0, reason = "dragon fail lev or food or corn need")

        #statue>600 lev,corn,defenceadd,pop,time
        #statuebuilding = [[27,80000,600,20,7200],[30,-8,700,40,14400]]
        if ground_id >=600 and ground_id <=605:
            print "build statue" + str(user_id)
            index = ground_id%600
            idlepop = user.population - user.labor_num
            if user.lev >= statuebuilding[index][0] and idlepop >= statuebuilding[index][3]:
                if statuebuilding[index][1]<0:
                    cost = 0 - statuebuilding[index][1]
                    if user.cae < cost:
                        return dict(id=0,reason="cae not enough")
                else:
                    cost = statuebuilding[index][1]
                    if user.corn < cost:
                        return dict(id=0,reason="corn not enough")
                #build
                statue = businessWrite(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = curTime, finish = 0)
                DBSession.add(statue)
                if statuebuilding[index][1]<0:
                    user.cae -= cost
                else:
                    user.corn -= cost
                user.labor_num += statuebuilding[index][3]
                user.defencepower += statuebuilding[index][2]
                read(city_id)
                return dict(id=1,result = "build statue suc")
            else:
                return dict(id=0,reason = "statue lev or pop failed")

        i=0
        price=0
        pricefood=0
        pop=0
        stone=0
        wood=0

        try:
            ca=0
            price=0
            pricefood=0
            pop=0
            ground_id=int(ground_id)
            stone=0
            wood=0
            m=0
            lis=getGround_id(int(ground_id))
            if lis==None:
                return dict(id=int(ground_id))
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime
            price=lis[0]
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            ######不能同时拥有两种相同神像
            p400=None;p401=None;p402=None;p403=None;p404=None;p405=None;p406=None;p400=None;p407=None;p408=None;p409=None;p410=None;p411=None;p412=None;p413=None;p414=None;p415=None;p416=None;p417=None;p418=None;p419=None
            if ground_id>=400 and ground_id<=499:
                try:
                    p400=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=400).all()
                    p401=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=401).all()
                    p402=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=402).all()
                    p403=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=403).all()
                    p404=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=404).all()
                    p405=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=405).all()
                    p406=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=406).all()
                    p407=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=407).all()
                    p408=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=408).all()
                    p409=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=409).all()
                    p410=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=410).all()
                    p411=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=411).all()
                    p412=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=412).all()
                    p413=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=413).all()
                    p414=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=414).all()
                    p415=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=415).all()
                    p416=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=416).all()
                    p417=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=417).all()
                    p418=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=418).all()
                    p419=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=419).all()
                    if (ground_id-400)%4==0:
                        if len(p400)!=0 or len(p404)!=0 or len(p408)!=0 or len(p412)!=0 or len(p416)!=0:
                            return dict(id=0)
                    elif (ground_id-400)%4==1:
                        if len(p401)!=0 or len(p405)!=0 or len(p409)!=0 or len(p413)!=0 or len(p417)!=0:
                            return dict(id=0,p401=p401,p405=p405,p413=p413,p417=p417)  
                    elif  (ground_id-400)%4==2:    
                        if len(p402)!=0 or len(p406)!=0 or len(p410)!=0 or len(p414)!=0 or len(p418)!=0:
                            return dict(id=0)    
                    elif  (ground_id-400)%4==3:    
                        if len(p403)!=0 or len(p407)!=0 or len(p411)!=0 or len(p415)!=0 or len(p419)!=0:
                            return dict(id=0)
                except:
                    xx=-1                                                
            if ground_id>=1 and ground_id<=499:
                pricefood=lis[1]
            if ground_id >=1 and ground_id<=99:
                pop=lis[2]
            elif ground_id>=200 and ground_id<399:
                pop=lis[2]
           
            if ground_id>=1 and ground_id<=99:
                wood=lis[3]
            elif ground_id>=100 and ground_id<=199:
                if lis[2]>0:
                    wood=lis[2]
                else:
                    stone=-lis[2]
            elif ground_id>=200 and ground_id<=299:
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
            elif ground_id>=300 and ground_id<=399:
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]        
            if price>=0:
                if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and ptime==0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.corn=u.corn-price
                    u.stone=u.stone-stone
                    u.wood=u.wood-wood
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    
                    p.finish=0
                    if ground_id>=1 and ground_id<=99:
                        p.finish=1
                        p.producttime=0
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                        p.producttime=ti
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                        p.producttime=ti
                    elif ground_id>=500 and ground_id<=599:
                        p.finish=1
                        p.producttime=0
                        u.populationupbound=u.populationupbound+lis[1]
                    elif ground_id>=400 and ground_id<=499:
                        m=1
                        u.populationupbound=u.populationupbound+lis[4]
                        u.exp=u.exp+lis[3] 
                        p.producttime=ti                     
                    else:
                        p.producttime=ti
                        
                    p.ground_id=int(ground_id)
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and ptime==0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    if u.cae+price<u.cae:
                        u.cae=u.cae+price
                        print inspect.stack()[0]
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    p.finish=0
                    if ground_id>=1 and ground_id<=99:
                        p.finish=1
                        p.producttime=0
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                        p.producttime=ti
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                        p.producttime=ti
                    elif ground_id>=500 and ground_id<=699:
                        p.finish=1
                        p.producttime=0
                        u.populationupbound=u.populationupbound+lis[1]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]
                        u.exp=u.exp+lis[3]
                        p.producttime=ti
                    else:
                        p.producttime=ti
                    #p.producttime=ti
                    p.ground_id=int(ground_id)
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
        except InvalidRequestError:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            ground_id=int(ground_id)
            if ground_id>=400 and ground_id<=499:
                try:
                    p400=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=400).all()
                    p401=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=401).all()
                    p402=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=402).all()
                    p403=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=403).all()
                    p404=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=404).all()
                    p405=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=405).all()
                    p406=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=406).all()
                    p407=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=407).all()
                    p408=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=408).all()
                    p409=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=409).all()
                    p410=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=410).all()
                    p411=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=411).all()
                    p412=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=412).all()
                    p413=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=413).all()
                    p414=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=414).all()
                    p415=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=415).all()
                    p416=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=416).all()
                    p417=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=417).all()
                    p418=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=418).all()
                    p419=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(ground_id=419).all()
                    if (ground_id-400)%4==0:
                        if len(p400)!=0 or len(p404)!=0 or len(p408)!=0 or len(p412)!=0 or len(p416)!=0:
                            return dict(id=0)
                    elif (ground_id-400)%4==1:
                        if len(p401)!=0 or len(p405)!=0 or len(p409)!=0 or len(p413)!=0 or len(p417)!=0:
                            return dict(id=0,p401=p401,p405=p405,p413=p413,p417=p417)  
                    elif  (ground_id-400)%4==2:    
                        if len(p402)!=0 or len(p406)!=0 or len(p410)!=0 or len(p414)!=0 or len(p418)!=0:
                            return dict(id=0)    
                    elif  (ground_id-400)%4==3:    
                        if len(p403)!=0 or len(p407)!=0 or len(p411)!=0 or len(p415)!=0 or len(p419)!=0:
                            return dict(id=0)
                except:
                    xx=-1             
            lis=getGround_id(int(ground_id))
            if lis[0]==None:
                return dict(id=-3)
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            price=lis[0]
            if ground_id>=1 and ground_id<=499:
                pricefood=lis[1]
            if ground_id >=1 and ground_id<=99:
                pop=lis[2]
            elif ground_id>=200 and ground_id<399:
                pop=lis[2]
            if ground_id>=1 and ground_id<=99:
                wood=lis[3]
            elif ground_id>=100 and ground_id<=199:
                if lis[3]!=0:
                    return dict(id='can not update')
                if lis[2]>0:
                    wood=lis[2]
                else:
                    stone=-lis[2]
            elif ground_id>=200 and ground_id<=299:
                if lis[4]!=0:
                    return dict(id='can not  update')
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
            elif ground_id>=300 and ground_id<=399:
                if lis[4]!=0:
                    return dict(id='can not update')
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
                    
            newbuilding=None
            if ground_id>=1 and ground_id<=99:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=0,finish=1)
            elif ground_id>=500 and ground_id<=699:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=0,finish=1)
            else:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
            if price>=0:
                if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.corn=u.corn-price
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    if ground_id>=1 and ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif ground_id>=500 and ground_id<=699:
                        u.populationupbound=u.populationupbound+lis[1]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]
                        u.exp=u.exp+lis[3]                        
                    DBSession.add(newbuilding)
                    c1=DBSession.query('LAST_INSERT_ID()')
                    #if ground_id==400 or ground_id==404 or ground_id==408 or ground_id==412:
                    #    u.food_god_lev=u.food_god_lev+1
                    #elif ground_id==401 or ground_id==405 or ground_id==409 or ground_id==413:
                    #    u.person_god_lev=u.person_god_lev+1
                    #elif ground_id==402 or ground_id==406 or ground_id==410 or ground_id==414:
                    #    u.wealth_god_lev=u.wealth_god_lev+1
                    #elif ground_id==403 or ground_id==407 or ground_id==411 or ground_id==415:
                    #    u.war_god_lev=u.war.god_lev+1
                    read(city_id)

                    replacecache(u.userid,u)#cache
                    return dict(id=1,gid=ground_id)
                else:
                    return dict(id=0)
            else:
                if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    if u.cae+price<u.cae:
                        u.cae=u.cae+price
                        print inspect.stack()[0]
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    if ground_id>=1 and ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]    
                        u.exp=u.exp+lis[3]                    
                    elif ground_id>=500 and ground_id<=699:
                        u.populationupbound=u.populationupbound+lis[1]
                    DBSession.add(newbuilding)
                    return dict(id=1)
                else:
                    return dict(id=0)

    @expose('json')
    def planting(self,user_id,city_id,grid_id,object_id,type):#对外接口，种植，资源获取operationalData:query->update; businessWrite:query->update
        try:
            if int(type)==0:
                price=Plant_Price[int(object_id)][0]
            elif int(type)==1:
                price=stones[int(object_id)][0]
            else:
                price=woods[int(object_id)][0]
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime
            if ptime>0:
                return dict(id=1)
            if price<0:
                sub=u.cae+price
                if sub>=0 and ptime==0:
                    #sub=u.cae
                    if u.cae>sub:
                        u.cae=sub#to update the datasheet
                        print inspect.stack()[0]
                    ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                    p.object_id=int(object_id)
                    p.producttime=ti
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            elif u.corn-price>=0  and ptime==0:
                sub=u.corn-price
                
                u.corn=sub#to update the datasheet
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                p.object_id=int(object_id)
                p.producttime=ti
                read(city_id)
                replacecache(u.userid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def harvest(self,user_id,city_id,grid_id,type):#对外接口，种植，资源收获warMap:query;operationalData:query->update; businessWrite:query->update
        try:
            type=int(type)
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            u=checkopdata(user_id)#cache
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            
            mark=minusstateeli(u,war,grid_id,p.producttime)
            mark=0
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            factor=1
            factor2=1.0
            if u.food_god==1 and t-u.foodgodtime<3600:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            elif u.food_god==2 and t-u.foodgodtime<21600:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            elif u.food_god==3 and t-u.foodgodtime<86400:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            else:
                u.food_god=0
                u.foodgodtime=-1                                
            tu=[]
            if p.ground_id==2:#水晶农田
                factor2=1.2
            elif p.ground_id==3:#宝石农田
                factor2=1.4
            elif p.ground_id==4:#精灵农田
                factor2=1.6
            if type==0:
                tu=Plant_Price[p.object_id]
            elif type==1:
                tu=stones[p.object_id]
            else:
                tu=woods[p.object_id]
            
                           
            if p.producttime!=1 and t-p.producttime>86400*3:
                p.producttime=0
                u.exp=u.exp+tu[1]
                p.object_id=-1 
                read(city_id)
                replacecache(u.userid,u)
                return dict(id=1)
            if type==0 and mark==0:
                tu=Plant_Price[p.object_id]
                
                u.food+=int(tu[2]*factor*(int(factor2*10))/10)
                DBSession.flush()
            elif type==1 and mark==0:
                tu=stones[p.object_id]
                u.stone=u.stone+int(tu[2]*factor)
            elif type==2 and mark==0:
                tu=woods[p.object_id]
                u.wood=u.wood+int(tu[2]*factor)
            u.exp=u.exp+tu[1]
            p.producttime=0
            p.object_id=-1
            
            read(city_id)
            replacecache(u.userid,u)#cache
            return dict(id=1,tu=tu[2])
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def plantingall(self,user_id,city_id,object_id):
        ground_num=0
        plant_list=[]
        try:
            u=checkopdata(user_id)#cache
            card = DBSession.query(Card).filter_by(uid=user_id).one()
            temp_cae = u.cae-1
            if temp_cae>=0 or card.foodcard==5:
                if card.foodcard==5:
                    temp_cae=temp_cae+1
                price=Plant_Price[int(object_id)][0]
                print inspect.stack()[0], object_id

                ground = DBSession.query(businessWrite).filter("city_id=:cid and producttime=0 and finish = 1 and ground_id <=4 and ground_id>=1").params(cid = int(city_id)).all()
                if ground==None or len(ground)==0:
                    return dict(id=0)
                if price<0:
                    price=0-price
                    temp_cae = temp_cae-price
                    if temp_cae < 0:
                        return dict(id=0)
                    temp_cae=temp_cae+price
                    for g in ground:
                        temp_cae=temp_cae-price
                        if temp_cae>=0:
                            plant_list.append(g.grid_id)
                            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                            g.object_id=int(object_id)
                            g.producttime=ti
                        else:
                            temp_cae = temp_cae+price
                            u.cae = temp_cae
                            return dict(id=1,plant=plant_list)
                    u.cae = temp_cae
                    return dict(id=1,plant=plant_list)
                else:
                    temp_corn = u.corn
                    if temp_corn-price < 0:
                        return dict(id=0)
                    for g in ground:
                        if temp_corn-price>=0:
                            temp_corn = temp_corn-price
                            plant_list.append(g.grid_id)
                            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                            g.object_id=int(object_id)
                            g.producttime=ti
                        else:
                            u.corn=temp_corn
                            u.cae=temp_cae
                            return dict(id=1,plant=plant_list)
                    u.corn=temp_corn
                    u.cae=temp_cae
                    return dict(id=1,plant=plant_list)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def harvestall(self,user_id,city_id):
        expadd=0
        foodadd=0
        flag=0
        try:
            u=checkopdata(user_id)#cache
            card = DBSession.query(Card).filter_by(uid=user_id).one()
            temp_cae = u.cae-1
            print inspect.stack()[0]

            if temp_cae>=0 or card.foodcard==5:
                if card.foodcard==5:
                    temp_cae=temp_cae+1
                map=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
                t=int(time.mktime(time.localtime())-time.mktime(beginTime))
                ground=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter("city_id=:cid and producttime>0 and finish = 1 and ground_id <=4 and ground_id>=1 and object_id>=0").params(cid = int(city_id)).all()
                if ground==None or len(ground)==0:
                    return dict(id=0)
                factor=1
                factor2=1.0
                if u.food_god==1 and t-u.foodgodtime<3600:
                    if u.food_god_lev==1:
                        factor=1.2
                    elif u.food_god_lev==2:
                        factor=1.4
                    elif u.food_god_lev==3:
                        factor=1.6
                    elif u.food_god_lev==4:
                        factor=1.8
                    elif u.food_god_lev==5:
                        factor=2
                elif u.food_god==2 and t-u.foodgodtime<21600:
                    if u.food_god_lev==1:
                        factor=1.2
                    elif u.food_god_lev==2:
                        factor=1.4
                    elif u.food_god_lev==3:
                        factor=1.6
                    elif u.food_god_lev==4:
                        factor=1.8
                    elif u.food_god_lev==5:
                        factor=2
                elif u.food_god==3 and t-u.foodgodtime<86400:
                    if u.food_god_lev==1:
                        factor=1.2
                    elif u.food_god_lev==2:
                        factor=1.4
                    elif u.food_god_lev==3:
                        factor=1.6
                    elif u.food_god_lev==4:
                        factor=1.8
                    elif u.food_god_lev==5:
                        factor=2
                else:
                    u.food_god=0
                    u.foodgodtime=-1
                for g in ground:
                    grid_id=g.grid_id
                    object_id=g.object_id
                    producttime=g.producttime
                    single_exp=Plant_Price[int(object_id)][1]
                    single_food=Plant_Price[int(object_id)][2]
                    growtime=Plant_Price[int(object_id)][3]
                    if g.ground_id==2:
                        factor2=1.2
                    elif g.ground_id==3:
                        factor2=1.4
                    elif g.ground_id==4:
                        factor2=1.6
                    if producttime+growtime<=t:
                        flag=1
                        mark=minusstateeli(u,map,grid_id,producttime)
                        if t-producttime>86400*3 and producttime!=1:
                            expadd = expadd+single_exp
                        else:
                            foodadd = foodadd+int(single_food*factor*(int(factor2*10))/10)
                            expadd = expadd+single_exp
                        g.object_id=-1
                        g.producttime=0
                    factor2=1.0
                u.exp=u.exp+expadd
                u.food=u.food+foodadd
                if flag==1:
                    u.cae = temp_cae
                read(city_id)
                replacecache(u.userid,u)#cache
                return dict(id=1,expadd=expadd,foodadd=foodadd)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def productall(self,user_id,city_id):
        expadd=0
        cornadd=0
        flag=0
        try:
            u=checkopdata(user_id)
            card = DBSession.query(Card).filter_by(uid=user_id).one()
            temp_cae = u.cae-1
            print inspect.stack()[0]

            if temp_cae>=0 or card.fortunecard==5:
                if card.fortunecard==5:
                    temp_cae=temp_cae+1
                map=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
                t=int(time.mktime(time.localtime())-time.mktime(beginTime))
                ground=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter("city_id=:cid and producttime>0 and finish = 1 and ground_id <=329 and ground_id>=300").params(cid = int(city_id)).all()
                if ground==None or len(ground)==0:
                    return dict(id=0)
                factor=1
                if u.wealth_god==1 and t-u.wealthgodtime<3600:
                    if u.wealth_god_lev==1:
                        factor=1.2
                    elif u.wealth_god_lev==2:
                        factor=1.4
                    elif u.wealth_god_lev==3:
                        factor=1.6
                    elif u.wealth_god_lev==4:
                        factor=1.8
                    elif u.wealth_god_lev==5:
                        factor=2
                elif u.wealth_god==2 and t-u.wealthgodtime<21600:
                    if u.wealth_god_lev==1:
                        factor=1.2
                    elif u.wealth_god_lev==2:
                        factor=1.4
                    elif u.wealth_god_lev==3:
                        factor=1.6
                    elif u.wealth_god_lev==4:
                        factor=1.8
                    elif u.wealth_god_lev==5:
                        factor=2
                elif u.wealth_god==3 and t-u.wealthgodtime<86400:
                    if u.wealth_god_lev==1:
                        factor=1.2
                    elif u.wealth_god_lev==2:
                        factor=1.4
                    elif u.wealth_god_lev==3:
                        factor=1.6
                    elif u.wealth_god_lev==4:
                        factor=1.8
                    elif u.wealth_god_lev==5:
                        factor=2
                else:
                    u.wealth_god=0
                    u.wealthgodtime=-1
                for g in ground:
                    grid_id = g.grid_id
                    producttime = g.producttime
                    single_exp = production[g.ground_id-300][1]
                    single_corn = production[g.ground_id-300][0]
                    needtime = production[g.ground_id-300][3]
                    if producttime+needtime<=t or producttime==1:
                        flag=1
                        mark=minusstateeli(u,map,grid_id,producttime)
                        if t-producttime>86400*3 and producttime!=1 and producttime!=0:
                            expadd = expadd + single_exp
                        else:
                            expadd = expadd+single_exp
                            cornadd = cornadd+int(single_corn*int(factor*10)/10)
                        g.producttime = t
                u.exp=u.exp+expadd
                u.corn = u.corn + cornadd
                if flag==1:
                    u.cae = temp_cae
                read(city_id)
                replacecache(u.userid,u)
                if flag==1:
                    return dict(id=1,expadd=expadd,cornadd=cornadd)
                else:
                    return dict(id=0)
            else:#cae not enough
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def getfriendall(self,user_id,friend_num,type):#type=0 normal;type=1 leiji
        print "getfriend "+str(user_id)
        uid = int(user_id)
        type = int(type)
        friend_num = int(friend_num)
        u = checkopdata(uid)
        cornadd = 0
        flag = 0
        bonus = 0
        k = 0#the number of the friend
        try:
            notvisited = DBSession.query(Papayafriend).filter_by(uid=uid).filter_by(visited=0).filter("lev > 0").all()
            if notvisited == None or len(notvisited)==0:
                return dict(id=0, reason="do not have not visited friend")
            card = DBSession.query(Card).filter_by(uid=uid).one()
            notvisited_num = len(notvisited)
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            mycity = DBSession.query(warMap).filter_by(userid = uid).one()
            #need the 424 god
            buildings = DBSession.query(businessWrite).filter("city_id=:cid and ground_id=424 and finish = 1").params(cid=mycity.city_id).all()
            print "friend god " + str(len(buildings))
            workTime = [3600, 21600, 86400]
            #only one friend god
            if len(buildings) > 0:
                b = buildings[0];
                if b.object_id >=0 and b.object_id < len(workTime) and workTime[b.object_id] > (t-b.producttime):
                    bonus = 50
                    print "friend God help"
                else:
                    b.object_id = -1
                    b.producttime = 0
            else:
                return dict(id=0,resaon="do not have the zijin god!")
            
            if type==0:#cae=2
                temp_cae = u.cae - 2
                print inspect.stack()[0]

                if temp_cae >= 0 or card.friendcard == 5:
                    flag = 1
                    if card.friendcard == 5:
                        temp_cae = temp_cae + 2
                    for f in notvisited:
                        k += 1
                        f.visited = 1
                    cornadd = (100 + bonus)*friend_num
                else:
                    return dict(id=0, reason="cae or card invalid")
            else:#cae=10 
                temp_cae = u.cae - 10
                print inspect.stack()[0]

                if temp_cae >=0:
                    flag = 1
                    for f in notvisited: 
                        cornadd += 100 + bonus + 5*k
                        k += 1
                        f.visited = 1
                    cornadd = (100+bonus)*friend_num + 5*(friend_num+1)*friend_num/2
            if flag == 1:
                u.corn = u.corn + cornadd
                u.cae = temp_cae
                read(mycity.city_id)
                return dict(id=1,cornadd=cornadd,getfriendnum=k)
            else:
                return dict(id=0,reason="do not get any friend")
        except InvalidRequestError:
            return dict(id=0, reason="invalid error")
    #build or upgrade finish both call this funciton
    @expose('json')
    def finish_building(self,user_id,city_id,grid_id):#对外接口，完成建筑物建造operationalData:query->update; businessWrite:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           lis=getGround_id(p.ground_id)
           u=checkopdata(user_id)#cache
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           if p.ground_id >= 420 and p.ground_id <= 424:
                if p.finish == 0:
                    lev = p.ground_id - 420
                    needTime = friendGod[lev][0]
                    if (ti-p.producttime) >= needTime:
                        p.object_id = -1
                        p.finish = 1
                        p.producttime = 0
                        return dict(id=1, result = "finish suc")
                return dict(id=0, reason="need more time or finish yet")
           if p.ground_id >= 600 and p.ground_id <= 605:
               if p.finish == 0:
                   index = p.ground_id -600
                   needTime = statuebuilding[index][4]
                   if (ti-p.producttime) >= needTime:
                       p.finish = -1
                       p.producttime = 0
                       return dict(id=1,result = "finish suc")
               return dict(id=0,reason="need more time or finish yet")

           if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412 or p.ground_id==416:
               if p.ground_id==400:
                   u.food_god_lev=1
               elif p.ground_id==404:
                   u.food_god_lev=2
               elif p.ground_id==408:
                   u.food_god_lev=3
               elif p.ground_id==412:
                   u.food_god_lev=4
               elif p.ground_id==416:
                   u.food_god_lev=5
           elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413 or p.ground_id==417:
               if p.ground_id==401:
                   u.person_god_lev=1
               elif p.ground_id==405:
                   u.persn_god_lev=2
               elif p.ground_id==409:
                   u.person_god_lev=3
               elif p.ground_id==413:
                   u.person_god_lev=4
               elif p.ground_id==417:
                   u.person_god_lev=5
           elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414 or p.ground_id==418:
               if p.ground_id==402:
                   u.wealth_god_lev=1
               elif p.ground_id==406:
                   u.wealth_god_lev=2
               elif p.ground_id==410:
                   u.wealth_god_lev=3
               elif p.ground_id==414:
                   u.wealth_god_lev=4
               elif p.ground_id==418:
                   u.wealth_god_lev=5
           else:
               if p.ground_id==403:
                   u.war_god_lev=1
               elif p.ground_id==407:
                   u.war_god_lev=2
               elif p.ground_id==411:
                   u.war_god_lev=3
               elif p.ground_id==415:
                   u.war_god_lev=4
               elif p.ground_id==419:
                   u.war_god_lev=5
           #if p.ground_id>=500 and p.ground_id<=699:
           #    u.populationupbound=u.populationupbound+lis[1]
           if p.ground_id>=300 and p.ground_id<=399:
               p.producttime=ti
           else:
               p.producttime=0        
           p.finish=1
           read(city_id)
           replacecache(u.userid,u)#cache
           return dict(id=1)
        except InvalidRequestError:
           return dict(id=0)
    def accCost(timeLeft):
        caesars = 0
        hour = 3600
        if timeLeft < 0:
                caesars = 0
        elif timeLeft < 3*hour:
                caesars = 1
        elif timeLeft < 6*hour:
                caesars = 2
        elif timeLeft < 9*hour:
                caesars = 3
        else:
                caesars = 5
        print "acc time " + str(timeLeft) + ' ' + str(caesars)
        return caesars   
    @expose('json')
    def speedup(self,user_id,city_id,grid_id):#对外接口，加速operationalData:query->update; businessWrite:query->update
        try:
            caesars=1
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            u=checkopdata(user_id)#cache
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            t=ti-p.producttime
            print "speed up " + str(user_id) + ' ' + str(city_id) + ' ' +str(grid_id) + ' ' + str(p.ground_id)
            if p.ground_id >= 420 and p.ground_id <= 424:
                if p.finish == 0:
                    lev = p.ground_id - 420
                    needTime = friendGod[lev][0]
                    timeLeft = needTime - t
                    cost = accCost(timeLeft)
                    if u.cae >= cost:
                        u.cae -= cost
                        print inspect.stack()[0]

                        p.object_id = -1
                        p.finish = 1
                        p.producttime = 0
                        DBSession.flush()
                        return dict(id=1, result = "firendgod finish suc", caeCost = cost)
                return dict(id=0, reason="friend god no work speed or finish yet")
            if p.ground_id >=600 and p.ground_id <=605:
                if p.finish == 0:
                    index = p.ground_id - 600
                    needTime = statuebuilding[index][4]
                    timeLeft = needTime - t
                    cost = accCost(timeLeft)
                    if u.cae >= cost:
                        u.cae -= cost
                        print inspect.stack()[0]

                        p.object_id = -1
                        p.finish = 1
                        p.producttime = 0
                        DBSession.flush()
                        return dict(id=1,result = "statue speedup suc",caeCost = cost)
                    return dict(id=0,reason="cae failed")
                return dict(id=0, reason="statue no work speed or finish yet")
            if p.ground_id==0:
                return dict(id=0, reason = "castal")
            elif  p.ground_id>=1 and p.ground_id<=99:
                if p.finish == 0:
                    p.finish = 1
                    read(city_id)
                    return dict(id=0, reason = "farm not finish")       
                else:
                    if p.object_id ==  -1:
                        return dict(id = 0, reason="not planting")
                    if p.ground_id < 5:
                        timeLeft=Plant_Price[p.object_id][3]-t
                    elif p.ground_id==5:
                        timeLeft=woods[p.object_id][3]-t
                    else:
                        timeLeft=stones[p.object_id][3]-t
                    caesars = accCost(timeLeft)
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        print inspect.stack()[0]

                        p.producttime=1#finish product
                        return dict(id=1,caesars=caesars,t=Plant_Price[p.object_id][3],t1=t, result = "farm speed har")
                    else:
                        return dict(id=0, reason = "farm cae not enu")
            elif p.ground_id>=100 and p.ground_id<=199:
                if p.finish==0:
                    timeLeft= housebuild[p.ground_id-100][5]-t
                    caesars = accCost(timeLeft)
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        print inspect.stack()[0]

                        p.producttime=0
                        p.finish=1
                        return dict(id=1,ca=caesars,cae=u.cae,h=housebuild[p.ground_id-100][5], result = "house fin")
                    else:
                        return dict(id=0, reason = "house fin cae not eno")
                else:
                    timeLeft = houses[p.ground_id-100][3]-t
                    caesars = accCost(timeLeft)
                    #0 not working 1 speedup yet
                    if p.producttime == 0 or p.producttime == 1:
                        return dict(id = 0, reason='house not working', pro = p.producttime)
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        print inspect.stack()[0]

                        p.producttime=1
                        return dict(id=1,caesars=caesars, result = "house pop")
                    else:
                        return dict(id=0, reason="house cae not")
            elif p.ground_id>=200 and p.ground_id<=299:
                if p.finish==0:
                    timeLeft = milbuild[p.ground_id-200][6]-t
                    caesars = accCost(timeLeft)
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        print inspect.stack()[0]

                        p.producttime=0
                        p.finish=1
                        return dict(id=1, result = "finish militry")
                    else:
                        return dict(id=0, reason = "mil cae not en")
                else:
                    if p.object_id>=0:
                        timeLeft = soldie[p.object_id][4]-t
                        caesars = accCost(timeLeft)
                        if u.cae-caesars>=0:
                            u.cae=u.cae-caesars
                            print inspect.stack()[0]

                            p.producttime=1
                            return dict(id=1, result = "mil product")
                        else:
                            return dict(id=0, reason = "mil not cae")
                    else:
                        return dict(id=0) 
            elif p.ground_id>=300 and p.ground_id<=399:
                if p.finish==0:
                    timeLeft = businessbuild[p.ground_id-300][6]-t
                    caesars = accCost(timeLeft)
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        print inspect.stack()[0]

                        p.producttime=ti
                        p.finish=1
                        return dict(id=1,caesars=caesars,t=businessbuild[p.ground_id-300][6], result = "business fin bui")
                    else:
                        return dict(id=0, reason = "busines not fin")
                else:
                    timeLeft = production[p.ground_id-300][3]-t
                    caesars = accCost(timeLeft)
                    if p.producttime == 1:
                        return dict(id = 0, reason = "busi speedup yet")
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=1
                        return dict(id = 1, result = "busi tax")
                    else:
                        return dict(id=0, reason = "busi cae not")     
            elif p.ground_id>=400 and p.ground_id<499:
                timeLeft = godbuild[p.ground_id-400][5]-t
                caesars = accCost(timeLeft)
                if p.finish==0 and u.cae-caesars>0:
                    u.cae=u.cae-caesars
                    print inspect.stack()[0]

                    p.producttime=0
                    if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412 or p.ground_id==416:
                        if p.ground_id==400:
                            u.food_god_lev=1
                        elif p.ground_id==404:
                            u.food_god_lev=2
                        elif p.ground_id==408:
                            u.food_god_lev=3
                        elif p.ground_id==412:
                            u.food_god_lev=4
                        elif p.ground_id==416:
                            u.food_god_lev=5
                    elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413 or p.ground_id==417:
                        if p.ground_id==401:
                            u.person_god_lev=1
                        elif p.ground_id==405:
                            u.persn_god_lev=2
                        elif p.ground_id==409:
                            u.person_god_lev=3
                        elif p.ground_id==413:
                            u.person_god_lev=4
                        elif p.ground_id==417:
                            u.person_god_lev=5
                    elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414 or p.ground_id==418:
                        if p.ground_id==402:
                            u.wealth_god_lev=1
                        elif p.ground_id==406:
                            u.wealth_god_lev=2
                        elif p.ground_id==410:
                            u.wealth_god_lev=3
                        elif p.ground_id==414:
                            u.wealth_god_lev=4
                        elif p.ground_id==418:
                            u.wealth_god_lev=5
                    else:
                        if p.ground_id==403:
                            u.war_god_lev=1
                        elif p.ground_id==407:
                            u.war_god_lev=2
                        elif p.ground_id==411:
                            u.war_god_lev=3
                        elif p.ground_id==415:
                            u.war_god_lev=4
                        elif p.ground_id==419:
                            u.war_god_lev=5                        
                    p.finish=1
                    read(city_id)
                    return dict(id=1, result = "god build fin")
                else:
                    return dict(id=0, reason = "god not enu")                  
            return dict(id = 0, reason = str(p.ground_id) + "can't speed")
        except InvalidRequestError:
            return dict(id=0, reason = "building not find")

    @expose('json')
    def population(self,user_id,city_id,grid_id):#对外接口，招募人口recruit population;operationalData:query->update; businessWrite:query->update
        try:
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            num=houses[p.ground_id-100][0]
            food=houses[p.ground_id-100][1]
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            
            u=checkopdata(user_id)#cache
            ptime=p.producttime
            if ptime>0:
                return dict(id=1)
            if u.food-food>=0:
                u.food=u.food-food
                p.producttime=ti
                p.object_id = 0
                read(city_id)
                replacecache(u.userid,u)#cache
                return dict(id=1)
            else :
                return dict(f=u.food-food,id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def finipop(self,user_id,city_id,grid_id):#对外接口，完成人口招募 finish population;warMap:query; operationalData,businessWrite:query->update
        try:
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            u=checkopdata(user_id)#cache
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            num=houses[p.ground_id-100][0]
            mark=minusstateeli(u,war,grid_id,p.producttime)
            mark=0
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            factor=1
            if p.producttime!=1 and t-p.producttime>3*86400:
                p.producttime=0
                p.object_id = -1
                u.exp=u.exp+houses[p.ground_id-100][2]
                read(city_id)
                replacecache(u.userid,u)#cache 
                return dict(id=1)               
            if u.person_god==1 and t-u.popgodtime<3600 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            elif u.person_god==2 and t-u.popgodtime<21600 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            elif u.person_god==3 and t-u.popgodtime<86400 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            else:
                u.person_god=0
                u.popgodtime=-1                                
            if mark==0:
                u.population=u.population+int(num*(int(factor*10))/10)
            p.producttime=0
            p.object_id = -1
            u.exp=u.exp+houses[p.ground_id-100][2]
            read(city_id)
            replacecache(u.userid,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def training(self,user_id,city_id,grid_id,sid):# 对外接口，训练士兵training soldiers; operationalData:query->update; businessWrite:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           i=int(sid)
           #three=soldier[i]
           corn=soldie[i][0]
           foo=soldie[i][1]
           pop=soldie[i][2]
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           ptime=p.producttime
           if ptime>0:
               return dict(id=1)
           if u.corn-corn>=0 and u.food-foo>=0 and u.population-pop>=u.labor_num and p.producttime==0 and p.finish==1:
               u.corn=u.corn-corn
               u.food=u.food-foo
               u.population=u.population-pop
               
               p.object_id=sid
               ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
               p.producttime=ti
               read(city_id)
               replacecache(u.userid,u)#cache
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def soldier(self,user_id,city_id,grid_id):#对外接口，完成士兵训练 finish training warMap:query;businessWrite,operationalData:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           sid=p.object_id
           mark=-1
           mark=minusstateeli(u,war,grid_id,p.producttime)
           mark=0
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           if p.producttime!=1 and ti-p.producttime>86400*3:
               p.producttime=0
               u.exp=u.exp+soldiernum[int(sid)]
               p.object_id=-1 
               read(city_id)
               replacecache(u.userid,u)
               return dict(id=1)           
           if mark==0 and int(sid)>=0 and int(sid)<9:
               if int(sid)>=0 and int(sid)<=2:
                   u.infantry1_num=u.infantry1_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]
               elif int(sid)>=3 and int(sid)<=5:
                   u.infantry2_num=u.infantry2_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]*2
               elif int(sid)>=6 and int(sid)<=8:
                   u.infantry2_num=u.infantry2_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]*3
           if mark==0 and int(sid)>=9 and int(sid)<18:
               if int(sid)>=9 and int(sid)<=11:
                   u.cavalry1_num=u.cavalry1_num+soldie[int(sid)][2]
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*4
                   print str(u.userid) + ' cav1 ' + str(soldie[int(sid)][2]*4)
               elif int(sid)>=12 and int(sid)<=14:
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*5
                   u.cavalry2_num=u.cavalry2_num+soldie[int(sid)][2]
                   print str(u.userid) + ' cav2 ' + str(soldie[int(sid)][2]*5)
               elif int(sid)>=15 and int(sid)<=17:
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*6
                   u.cavalry3_num=u.cavalry3_num+soldie[int(sid)][2]
                   print str(u.userid) + ' cav3 ' + str(soldie[int(sid)][2]*6)
           if mark==0 and int(sid)>=18 :
               if int(sid)>=18 and int(sid)<=20:
                   u.scout1_num=u.scout1_num+soldie[int(sid)][2]
               elif int(sid)>=21 and int(sid)<=23:
                   u.scout2_num=u.scout2_num+soldie[int(sid)][2]
               else:
                   u.scout3_num=u.scout3_num+soldie[int(sid)][2]
           u.exp=u.exp+soldiernum[int(sid)]
           p.producttime=0
           p.object_id=-1
           read(city_id)
           replacecache(u.userid,u)#cache
           return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def product(self,user_id,city_id,grid_id):# 对外接口，生产business produce warMap:query businessWrite:query->update operationalData:update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
           mark=minusstateeli(u,war,grid_id,p.producttime)
           mark=0
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           factor=1
           if p.producttime!=1 and p.producttime!=0 and ti-p.producttime>3*86400:
               u.exp=u.exp+production[p.ground_id-300][1]
               p.producttime=ti
               read(city_id)
               replacecache(u.userid,u)#cache
               return dict(id=1)               
           if ti-p.producttime>=production[p.ground_id-300][3] or p.producttime==0:#time
               if u.wealth_god==1 and ti-u.wealthgodtime<3600:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2
               elif u.wealth_god==2 and ti-u.wealthgodtime<21600:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2
               elif u.wealth_god==3 and ti-u.wealthgodtime<86400:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2 
               else:
                   u.wealth_god=0
                   u.wealthgodtime=-1                                    
               if mark==0:
                   u.corn=u.corn+int(production[p.ground_id-300][0]*int(factor*10)/10)
               u.exp=u.exp+production[p.ground_id-300][1]
               p.producttime=ti
               read(city_id)
               replacecache(u.userid,u)#cache
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def expand(self,user_id,city_id,type):#对外接口，扩地operationalData:query->update
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            type=int(type)
            if u.landkind==EXPANDLEV :
                return dict(id=-2)
            if type==0:
                u.landkind=u.landkind+1
            elif type==2:
                corn=expanding[u.landkind][0]
                if u.corn-corn>=0:
                    u.corn=u.corn-corn
                    u.landkind=u.landkind+1
                else:
                    return dict(id=0)
            else:
                cae=expanding[u.landkind][1]
                if u.cae-cae>=0:
                    u.cae=u.cae-cae
                    print inspect.stack()[0]
                    u.landkind=u.landkind+1
                else:
                    return dict(id=0)
            u.exp=u.exp+expanding[u.landkind-1][2]
            replacecache(u.userid,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def retlev(self,uid):
        fs=[]
        try:
            x=DBSession.query(Papayafriend).filter_by(uid=int(uid)).all()
            for xx in x:
                fs.append(xx)
            return dict(friendlist=fs)
        except:
            return dict(friendlist=fs)
    @expose('json')
    def addppyfriend(self,uid,rrstring):#对外接口，返回好友等级operationalData:query
        f=None
        s=''
        ukind=0
        try:
            dict0={}
            list1=rrstring.split(';')
            for string2 in list1 :
                list2=string2.split(',')
                oid=list2[0]#otherid 为varchar类型
                ukind=int(list2[1])
                try:
                    uu=DBSession.query(operationalData).filter_by(otherid=oid).filter_by(user_kind=ukind).one()
                    um=checkopdata(int(uid))
                    try:
                        uff=DBSession.query(Papayafriend).filter_by(uid=int(uid)).filter_by(papayaid=oid).filter_by(user_kind=uu.user_kind).one()
                    except InvalidRequestError:
                        #return dict(id=11)
                        uf1=Papayafriend(uid=int(uid),papayaid=oid,lev=uu.lev,user_kind=uu.user_kind)
                        DBSession.add(uf1)
                    try:
                        uff=DBSession.query(Papayafriend).filter_by(uid=uu.userid).filter_by(papayaid=um.otherid).filter_by(user_kind=um.user_kind).one()
                    except InvalidRequestError:
                        uf2=Papayafriend(uid=uu.userid,papayaid=um.otherid,lev=um.lev,user_kind=um.user_kind)
                        DBSession.add(uf2)                        
                    #uf2=Papayafriend(uid=int(uid),papayaid=oid,lev=uu.lev,user_kind=uu.user_kind)
                    v=0
                    #uf=checkopdata(uu.userid)#cache
                    #s=s+str(uf.lev)+","+str(v)+";"
                    if uu!=None:
                        dict0[list2[0]]=dict(level=uu.lev,visited=v)
                    else:
                        dict0[list2[0]]=dict(level=-1)
                except InvalidRequestError:
                    try:
                        uff=DBSession.query(Papayafriend).filter_by(uid=int(uid)).filter_by(papayaid=oid).filter_by(user_kind=ukind).one()
                    except:
                        uf1=Papayafriend(uid=int(uid),papayaid=oid,lev=-1,user_kind=ukind)
                        DBSession.add(uf1)                
                    dict0[list2[0]]=dict(level=-1)
            return dict0
        except InvalidRequestError:
            return dict(id=0)         
    @expose('stchong.templates.help')      
    def help(self):
        return dict(page='help')
    @expose('stchong.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('stchong.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('stchong.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('stchong.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('stchong.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('stchong.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('stchong.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('stchong.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
