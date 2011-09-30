import urllib
import exceptions
import MySQLdb
import json
try:
    con = MySQLdb.connect(host='localhost', user='root', db='stcHong')
except:
    print "con error"
cursor = con.cursor()
sql = 'select userid from operationalData'
cursor.execute(sql)
data = cursor.fetchall()
req = 'http://localhost:8088/war/'
for uid in data:
    try:
        war = req + str(uid[0])
        print war
        res = urllib.urlopen(war)
        response = res.read()
        print response
    except:
        print "visit user " + str(uid[0]) + ' fail'

