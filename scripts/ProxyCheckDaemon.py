#!/usr/bin/python3
# -*- coding: utf-8 -*-
######################################################################################
#                                                                                    #
# Автоматическая проверка активных прокси серверов данные для анализа                #
# получаются из базы данных http_proxy.sqlite, после проверки выставляется           #
# флаг Active, а в лучае доступности сервиса запись активности добавляется           #
# в центральную базу (так-же добавляется запись о последнем времени проверки)        #
# Когда данные для анализа заканчиваются все флаги Active в базе sqlite сбрасываются #
# и проверка запускается заново.                                                     #
#                                                                                    #
######################################################################################
import sqlite3
import os
import json
import datetime
from DatabaseLibs import DatabaseConnection
from WebElements import ProxyRequestPage

script_path=os.path.dirname( __file__ )
try:
	con = sqlite3.connect(script_path+"/../data/http_proxy.sqlite")
	cur = con.cursor()
	cur.execute("SELECT ip,port FROM http_proxy WHERE active='False' ORDER BY RANDOM() LIMIT 1;")
	data=cur.fetchone()
	cur.close()
	con.close()
except:
	data=['','']
if data!=None:
	try:
		con = sqlite3.connect(script_path+"/../data/http_proxy.sqlite")
		cur = con.cursor()
		cur.execute("UPDATE http_proxy SET active='True' WHERE ip='"+str(data[0])+"' AND port="+str(data[1])+";")
		con.commit()
		cur.close()
		con.close()
		result=(str(ProxyRequestPage('http://acisi.ru/api/?action=webinfo',str(data[0]),str(data[1])).data,'utf-8'))
	except:
		result=''
	if result!='':
		try:
			json_result=json.loads(result)[1]['AcisiProject']
		except:
			json_result=''
		if json_result=='READY':
			conn=DatabaseConnection()
			curr=conn.cursor()
			try:
				curr.execute('INSERT INTO acisi_http_proxy(ip,port) VALUES (\''+str(data[0])+'\','+str(data[1])+')')
				conn.commit()
				status=True
			except:
				status=True
				conn.commit()
			try:
				curr.execute('UPDATE acisi_http_proxy SET active=True, lastcheck=\''+str(datetime.datetime.now())+'\' WHERE ip=\''+str(data[0])+'\' AND port='+str(data[1])+';')
				conn.commit()
				status=True
			except:
				status=True
			curr.close()
			conn.close()
		else:
			conn=DatabaseConnection()
			curr=conn.cursor()
			try:
				curr.execute('UPDATE acisi_http_proxy SET active=False WHERE ip=\''+str(data[0])+'\' AND port='+str(data[1])+';')
				conn.commit()
				status=True
			except:
				status=True
			curr.close()
			conn.close()
else:
	con = sqlite3.connect(script_path+"/../data/http_proxy.sqlite")
	cur = con.cursor()
	cur.execute("UPDATE http_proxy SET active='False';")
	con.commit()
	cur.close()
	con.close()
