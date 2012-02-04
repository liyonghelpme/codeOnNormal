import MySQLdb
con = MySQLdb.connect(host='223.4.87.9', user='root', passwd='2e4n5k2w2x', db='stcHong')
cursor = con.cursor()
sql = 'select mapid from warMap  where mapid != -1 group by mapid'
cursor.execute(sql)
data = cursor.fetchall()
for d in data:
    #print d[0]
    sql = 'select userid, map_kind from warMap where mapid = ' + str(d[0])
    cursor.execute(sql)
    res = cursor.fetchall()
    mapkind = set()
    for r in res:
        mapkind.add(r[1])
    l = len(mapkind)
    if l > 1:
        print d[0], l
