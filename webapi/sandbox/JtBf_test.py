# cat employee.py 
import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='D1spers1ve',
         host='172.16.60.1',
         database='AutoDB')

cur = conn.cursor()

query = ("SELECT * FROM test")

cur.execute(query)

for (A, B, C) in cur:
  print("{}, {}, {}".format(A, B, C))

cur.close()
conn.close()
