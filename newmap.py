import MySQLdb
import json
con = MySQLdb.connect(host="223.4.87.9", user='root', passwd='2e4n5k2w2x', db='stcHong')
cursor = con.cursor()
def exe(sql):
    print sql
    cursor.execute(sql)
mapkind = 0
sql = 'select mapid, count(*) from warMap where map_kind = '+str(mapkind) +' group by mapid'
exe(sql)
data = cursor.fetchall()

gids = 0
total = 30
newmap = 1900
for d in data:
    if d[1] < 3:
        sql = 'select userid, map_kind from warMap where mapid = ' + str(d[0]) + ' and map_kind = '+str(mapkind)
        exe(sql)
        seUsers = cursor.fetchall()
        for u in seUsers:
            sql = 'update warMap set mapid = '+ str(newmap)+', gridid = '+str(gids)+ ' where userid = ' + str(u[0]) + ' and mapid = '+ str(d[0])
            exe(sql)
            gids += 1
            if gids >= total:
                break
    if gids >= total:
        break
    
con.commit()
