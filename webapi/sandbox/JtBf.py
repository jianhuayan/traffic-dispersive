# cat employee.py 
import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='D1spers1ve',
         host='172.16.60.1',
         database='AutoDB')

cur = conn.cursor()

query = ("SELECT * FROM JtBf_set")

cur.execute(query)

for (TestNum, Delay, Jitter, Packetloss) in cur:
  print("{}, {}, {}, {}".format(TestNum, Delay,Jitter,Packetloss))

cur.close()
conn.close()
