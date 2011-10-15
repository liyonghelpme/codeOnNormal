import os,sys,string
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='badperson3',db='stcHong')
except Exception, e:
    print e
    sys.exit()
cursor=conn.cursor()    
sql="delete from news"
try:
    cursor.execute(sql)
except Exception, e:
    print e
    sys.exit()
    
conn.commit()