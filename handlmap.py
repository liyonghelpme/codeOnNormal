import json
import MySQLdb
f = file('res2.txt', 'r').read()
d = json.loads(f)
con = MySQLdb.connect(host='223.4.87.9', user='root', passwd='2e4n5k2w2x', db='stcHong')
cursor = con.cursor()

res = {}
for k in d:
    sql = 'select userid, map_kind from warMap where mapid = '+k
    cursor.execute(sql)
    out = cursor.fetchall()
    res[k] = []
    for r in out:
        res[k].append(r)
f = file('res3.txt', 'w')
f.write(json.dumps(res))
