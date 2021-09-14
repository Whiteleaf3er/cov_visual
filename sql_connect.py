#!/usr/bin/python

import psycopg2
import time
import json

conn = psycopg2.connect(database="cov_0910", user="postgres", password="Lh@990607", host="127.0.0.1", port="5432")

print("Opened database successfully")

cur = conn.cursor()
# sql = "INSERT INTO history VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# cur.execute(sql,[time.strftime("%Y-%m-%d"),10,1,2,3,4,5,6,7])
# conn.commit()
sql="select * from history"
cur.execute(sql)
res = cur.fetchall()
print(res)
cur.close()
conn.close()



# cur.execute('''CREATE TABLE details
#        (
#        id SERIAL PRIMARY KEY NOT NULL,
# update_time char(100) DEFAULT NULL ,
# province varchar(15) DEFAULT NULL ,
# city varchar(15) DEFAULT NULL ,
# confirm int DEFAULT NULL ,
# confirm_add int DEFAULT NULL ,
# heal int DEFAULT NULL ,
# dead int DEFAULT NULL );'''
#             )
# print ("Table created successfully")

# conn.commit()
# conn.close()

