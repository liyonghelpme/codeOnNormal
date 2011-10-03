import MySQLdb
con = MySQLdb.connect(host='localhost', user='root', db='stcHong')
cursor = con.cursor()
sql = "select uid, woninmap, bwon from ( select victories.uid, woninmap, count(*) as bwon from victories, occupation where victories.uid = occupation.masterid group by victories.uid) as temp where temp.woninmap < temp.bwon"
cursor.execute(sql)
res = cursor.fetchall()
for data in res:
    print str(data)
    uid = data[0]
    bwon = data[2]
    sql = "update victories set woninmap = "+str(bwon) + ' where uid= ' + str(uid);
    cursor.execute(sql)
    con.commit()
