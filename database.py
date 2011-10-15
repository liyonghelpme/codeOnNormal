import os,sys,string
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='badperson3',db='stcHong')
except Exception, e:
    print e
    sys.exit()
    

        
cursor=conn.cursor()

sql="update operationalData set visitnum=0;"
cursor.execute(sql)

sql="update papayafriend set visited=0"
try:
    cursor.execute(sql)
except Exception,e:
    print e
    sys.exit()
    
sql="update visitFriend set visited=0"
try:
    cursor.execute(sql)
except Exception, e:
    print e
    sys.exit()
    
sql="update datevisit set visitnum=0;"
cursor.execute(sql)  
    
sql="update operationalData set datesurprise=0"
try:
    cursor.execute(sql)
except Exception, e:
    print e
    sys.exit()   
    
sql="update operationalData set monfood=0"
try:
    cursor.execute(sql)
except Exception,e:
    print e
    sys.exit() 

sql="update datesurprise set datesurprise=0"
try:
    cursor.execute(sql)
except Exception, e:
    print e
    sys.exit()

sql="update datesurprise set monfood=0"
try:
    cursor.execute(sql)
except Exception,e:
    print e
    sys.exit()
sql="update datevisit set visitnum=0;"
cursor.execute(sql)    
    
conn.commit()
