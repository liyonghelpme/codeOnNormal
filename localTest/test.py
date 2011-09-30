#simulate user to access each interface
#simulate A liyongtestFormal0  attack B liyongtestFormal1
import urllib
import exceptions
import MySQLdb
import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from json import JSONDecoder
interfaces = ['logsign/', 'logsign/',  'war/', 'logsign/', 'logsign/', 'attack/', 'attackspeedup/', 'war/']
responses = ['md51', 'id', 'battleresult', 'md51', 'id', 'id', 'id', 'battleresult']
md51 = 0
userid = 0
infPow = 0
cavPow = 0
battleRes = ''
base = 'http://localhost:8088/'
i = 0

md52 = 0
id2 = 0

myname = raw_input()
enename = raw_input()
try:
    conn = MySQLdb.connect(host='localhost', user='root', db='stcHong')
except:
    print "con error"
cursor = conn.cursor()
state = 0
while i < len(interfaces):
    try:
        test = ''
        domain = base + interfaces[state]
        if state == 0:
            test = urllib.urlopen(domain + myname +"/0/0")
        elif state == 1:
            test = urllib.urlopen(domain +  myname + "/0/"+md51)
        elif state == 2:
            test = urllib.urlopen(domain + str(userid))
        elif state == 3:
            test = urllib.urlopen(domain + enename + '/0/0')
        elif state == 4:
            test = urllib.urlopen(domain + enename + '/0/'+md52)
        elif state == 5:
            test = urllib.urlopen(domain +str(userid) + '/' + str(id2) + '/1000/' + str(infPow) + '/' + str(cavPow))
        elif state == 6:
            test = urllib.urlopen(domain + str(userid) + '/' + str(id2))
        elif state == 7:
            test = urllib.urlopen(domain + str(userid))
        data = test.read()
        print "data " + str(data)
        res = json.loads(data)
        print "result response " + str(res[responses[state]])
        if state == 0:
            md51 = res['md51']
        elif state == 1:
            userid = res['id']
            sql = "update operationalData set cae = 1000, infantrypower=1000 where userid = " + str(userid)
            cursor.execute(sql)
            conn.commit()
            
            infPow = 1000
            cavPow = res['cavalrypower']
        elif state == 2:
            battleRes = res['battleresult']
        elif state == 3:
            md52 = res['md51']
        elif state == 4:
            id2 = res['id']
            sql = "update operationalData set cae = 1000 where userid = " + str(id2)
            cursor.execute(sql)
            conn.commit()
        elif state == 5:
            print ''
        elif state == 6:
            print ''
        elif state == 7:
            battleRes = res['battleresult']
        print "suc " + str(i) + ' ' + interfaces[i]
    except:
        print "fail " + str(i) + ' ' + interfaces[i]
    state += 1
    i += 1
