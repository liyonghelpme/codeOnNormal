import urllib
import MySQLdb
import json
import time
#test 1 A attack B A win uid 1 uid2
#not occupation 
#update victories
my = raw_input()
ene = raw_input()
con = MySQLdb.connect(host='localhost', user='root', db='stcHong')
cursor = con.cursor()
sql = "update operationalData set infantrypower=10000, cae=10000 where userid = " + my
cursor.execute(sql)
con.commit()

domain = 'http://localhost:8088/'
req = domain + 'attack/'+my+'/'+ene+'/1000/10000/0'
res = urllib.urlopen(req)
res = res.read()
print 'attack ' + str(res)
time.sleep(1)
while True:
    req = domain + 'attackspeedup/'+my+'/'+ene
    res = urllib.urlopen(req)
    res = res.read()
    print 'attack speed ' + str(res)
    res = json.loads(res)
    if int(res['id']) == 1:
        break

req = domain+'war/'+my
res = urllib.urlopen(req)
res = res.read()
print 'war result ' + str(res)

sql = "select * from victories where uid = " +my
cursor.execute(sql)
con.commit()
myState = cursor.fetchall()

sql = "select * from victories where uid = " + ene
cursor.execute(sql)
con.commit()
eneState = cursor.fetchall()

for s in myState:
    print str(s)
for e in eneState:
    print str(e)
sql = "select * from occupation where masterid=" + my
cursor.execute(sql)
con.commit()
occ = cursor.fetchall()
for o in occ:
    print str(o)
