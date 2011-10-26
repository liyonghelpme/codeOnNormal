import MySQLdb

con = MySQLdb.connect(host='localhost', user='root', db='stcHong')
cursor = con.cursor()

sql = "update warMap set minusstate = \"\""
cursor.execute(sql)
con.commit()
