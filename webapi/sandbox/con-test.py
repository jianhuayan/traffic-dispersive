#! /usr/bin/python2.7
import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='D1spers1ve',
         host='172.16.60.1',
         database='AutoDB')

conn.close()
