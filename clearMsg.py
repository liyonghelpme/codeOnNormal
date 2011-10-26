import MySQLdb
import json
import time

con = MySQLdb.connect(host='localhost', user='root', db='stcHong', passwd='2e4n5k2w2x')
cursor = con.cursor()

beginTime = [2011, 1, 1, 0, 0, 0, 0, 0, 0]
curNow = int(time.mktime(time.localtime()) - time.mktime(beginTime))

thDays = 3*24*3600
unReadNum = 100

#remove read
sql = 'delete from message where `read` = 1 and ('+str(curNow)+ '  - time) > '+ str(thDays)
cursor.execute(sql)

#get all user unread > 100
sql = 'select fid, num from ( select fid, count(*) as num from message group by fid) as temp where num > ' + str(unReadNum)
cursor.execute(sql)
data = cursor.fetchall()
print data

for d in data:
    num = d[1]
    remove = num - unReadNum
    print "remove " + str(remove)
    sql = 'delete from message where fid = ' + str(d[0]) + ' order by time limit ' + str(remove)
    cursor.execute(sql)
con.commit()
