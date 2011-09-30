import MySQLdb
import urllib
import json

interfaces = ['logsign/', 'logsign/', 'logsign/', 'logsign/', 'attack/', 'upgrademap/']
id1 = 0
id2 = 0
md5 = 0
base = ''
con = MySQLdb.connect(host='localhost', user='root', db='stcHong')
cursor = con.cursor()
state = 0
i = 0
my = raw_input()
en = raw_input()
for inf in interfaces:
    test = ''
    domain = 'http://localhost:8088/'+inf
    req = domain
    if state == 0:
        req = domain+my+'/0/0'
    elif state == 1:
        req = domain+my+'/0/' + str(md5)
    elif state == 2:
        req = domain+en+'/0/0'
    elif state == 3:
        req = domain+en+'/0/'+str(md5)
    elif state == 4:
        req = domain+str(id1)+'/'+str(id2) + '/1000/10000/0'
    elif state == 5:
        req = domain+str(id1)
    test = urllib.urlopen(req)
    res = test.read()
    print 'data ' + str(res)
    res = json.loads(res)
    
    if state == 0:
        md5 = res['md51']
    elif state == 1:
        id1 = res['id']
        sql = "update operationalData set cae = 1000, infantrypower = 10000, nobility =0  where userid = " + str(id1)
        cursor.execute(sql)
        con.commit()
        sql = "update victories set woninmap = 4 where uid = "+str(id1)
        cursor.execute(sql)
        con.commit()

    elif state == 2:
        md5 = res['md51']
    elif state == 3:
        id2 = res['id']
    elif state == 4:
        print 'attack ' + str(res['id'])
    elif state == 6:
        print 'upgrade ' + str(res['id'])
    state += 1

