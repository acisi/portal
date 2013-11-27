#!/usr/bin/python3
import psycopg2
conn_string = "host='127.0.0.1' dbname='portal' user='portal' password='killa11'"
conn=psycopg2.connect(conn_string)
curr=conn.cursor()
curr.execute('SELECT text FROM acisi_anekdot')
anekdots=curr.fetchall()
f = open('./anekdot_list.txt','w')
for anekdot in anekdots:
	print (anekdot[0])
	f.write(anekdot[0])
	print ("=============================================\n")
	f.write('\n'+'==[acisi]=='+'\n')
f.close()
curr.close()
conn.close()