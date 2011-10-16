#!/usr/bin/env python   
#coding=utf-8

import MySQLdb
#import pickle
import time

absTime = (2011,1,1,0,0,0,0,0,0)
endTime = time.localtime()
time2 = int(time.mktime(endTime)-time.mktime(absTime))
time1 = time2-86400
beginTime = time.localtime(time1+time.mktime(absTime))

conn = MySQLdb.connect(host='localhost',user='root',passwd='badperson3',db='stcHong')
cursor = conn.cursor()
file = open("/root/linan-empire/buycae.log","a")
file.write("################ buy cae daily report--"+time.strftime("%Y-%m-%d %H:%M:%S ",beginTime)+"~"+time.strftime("%Y-%m-%d %H:%M:%S ",endTime)+" ##################\n")
file.write("The beginTime is "+str(time1)+"\n")
file.write("The endTime is "+str(time2)+"\n")
#print "################ wonder_empire daily report--"+time.strftime("%Y-%m-%d %H:%M:%S ",beginTime)+"~"+time.strftime("%Y-%m-%d %H:%M:%S ",endTime)+" ##################"

sql = "select * from caebuy where cae > 3 and time < %s and time > %s"
param=(time2,time1)
cursor.execute(sql,param)
i = 0
cae = 0
results = cursor.fetchall()
for r in results:
#    file.write(r[0])
    cae = cae + r[1]
    i = i+1
#    print r
    file.write(str(r)+"\n")
#print "Daily number of users who buy caes(>3): "+str(i)
file.write("Daily number of users who buy caes(>3): "+str(i)+"\n")
file.write("Daily caes(>3) buy:"+str(cae)+"\n")
#print "Daily caes(>3) buy:"+str(cae)
#pickle.dump(result,file)
#print result

sql = "select * from caebuy where cae > 3 and time < %s"
param=(time2)
cursor.execute(sql,param)
cae = 0
i = 0
results = cursor.fetchall()
for r in results:
#    file.write(r[0])
    cae = cae + r[1]
    i = i+1
#    print r
#print "Total number of users who buy caes >3 :"+str(i)
#print "Total caes(>3) buy:"+str(cae)
file.write("Total number of users who buy caes >3 :"+str(i)+"\n")
file.write("Total caes(>3) buy:"+str(cae)+"\n")

sql = "select * from caebuy where time < %s and time > %s"
param=(time2,time1)
cursor.execute(sql,param)
cae = 0
i = 0
results = cursor.fetchall()
for r in results:
#    file.write(r[0])
    cae = cae + r[1]
    i = i+1
#    print r
#print "Daily number of users who buy caes:"+str(i)
#print "Daily caes buy:"+str(cae)
file.write("Daily number of users who buy caes:"+str(i)+"\n")
file.write("Daily caes buy:"+str(cae)+"\n")

sql = "select * from caebuy where time < %s"
param=(time2)
cursor.execute(sql,param)
cae = 0
i = 0
results = cursor.fetchall()
for r in results:
#    file.write(r[0])
    cae = cae + r[1]
    i = i+1
#    print r
#print "Total number of users who buy caes: "+str(i)
file.write("Total number of users who buy caes: "+str(i)+"\n")
#print "Total caes buy:"+str(cae)
file.write("Total caes buy:"+str(cae)+"\n")

#sql = "select count(*) from caebuy where cae > 3 and time < %s and time > %s "
#param=(time2,time1)
#cursor.execute(sql,param)
#result = cursor.fetchall()
#file.write("Daily User's buying cae Number:")
#for r in results:
#    file.write(r[0])
#    print r
#print result
#pickle.dump(result,file)

sql = "select userid from operationalData where signtime < %s and signtime > %s"
param=(time2,time1)
cursor.execute(sql,param)
i = 0
results = cursor.fetchall()
for r in results:
    i = i+1
#print "Daily number of New Users:"+str(i)
file.write("Daily number of New Users:"+str(i)+"\n")

sql = "select userid from operationalData where lev >= 3 and signtime < %s and signtime > %s"
param=(time2,time1)
cursor.execute(sql,param)
i = 0
results = cursor.fetchall()
for r in results:
    i = i+1
#print "Daily number of New Users and Lev>=3: "+str(i)
file.write("Daily number of New Users and Lev>=3: "+str(i)+"\n")

sql = "select userid from operationalData where userid > 3260"
#param=(time2,time1)
cursor.execute(sql)
i = 0
results = cursor.fetchall()
for r in results:
    i = i+1
#print "Total number of New Users:"+str(i)
file.write("Total number of New Users:"+str(i)+"\n")

sql = "select userid from operationalData where logintime < %s and logintime > %s"
param=(time2,time1)
cursor.execute(sql,param)
i = 0
results = cursor.fetchall()
for r in results:
    i = i+1
#print "Daily number of Login Users: "+str(i)
file.write("Daily number of Login Users: "+str(i)+"\n\n")

file.close()
cursor.close()
conn.close()
#file.close()

