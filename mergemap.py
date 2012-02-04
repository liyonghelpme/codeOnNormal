import MySQLdb
import json
con = MySQLdb.connect(host="223.4.87.9", user='root', passwd='2e4n5k2w2x', db='stcHong')
cursor = con.cursor()

def exe(sql):
    print sql
    cursor.execute(sql)
sql = 'select mapid, count(*) from warMap where map_kind = 2 group by mapid'
exe(sql)
data = cursor.fetchall()

mapNum = 60
lastMap = -1
gid = []
usercount = 0
for d in data:
    if d[1] < 10:
        sql = 'select mapid, count(*) from warMap where mapid = ' + str(d[0])
        cursor.execute(sql)
        mapinfo = cursor.fetchall()
        for m in mapinfo:
            print d[0], d[1], m[1]
            usercount += d[1]
print usercount

            
        
        
