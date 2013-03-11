import MySQLdb
import json
con = MySQLdb.connect(host="223.4.87.9", user='root', passwd='2e4n5k2w2x', db='stcHong')
cursor = con.cursor()

sql = 'select mapid, count(*) from warMap where map_kind = 1 group by mapid'
cursor.execute(sql)
allMap = cursor.fetchall()
for aMap in allMap:
    if aMap[1] < 10:
        sql = 'select userid, map_kind from warMap where mapid = ' + str(aMap[0])
        cursor.execute(sql)
        data = cursor.fetchall()
        maxnob = -1000
        notEqual = []
        for d in data:
            sql = 'select nobility from operationalData where userid = '+str(d[0])
            cursor.execute(sql)
            res = cursor.fetchall()
            if len(res) == 0:
                continue
            for n in res:
                nob = n[0]
            if nob > maxnob:
                maxnob = nob
            if nob != d[1]:
                print d[0], nob, d[1]
                sql = 'update warMap set map_kind = '+str(nob) +' where userid = ' + str(d[0]) + ' and mapid = ' + str(aMap[0])
                print sql
                cursor.execute(sql)
        print "max", maxnob

