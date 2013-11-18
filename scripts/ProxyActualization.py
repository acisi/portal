#!/usr/bin/python3
# -*- coding: utf-8 -*-
####################################################################################
#                                                                                  #
# Актуализация базы уже проверенных прокси                                         #
# Работаем с боевой базой, проверяем прокси которые давно не проверялись           #
# изменяем исколчительно флаг активности и дату проверки.                          #
#                                                                                  #
####################################################################################
import os
import json
import datetime
from DatabaseLibs import DatabaseConnection
from WebElements import ProxyRequestPage

script_path=os.path.dirname( __file__ )
isactive=False
operationok=False
try:
	con=DatabaseConnection()
	cur=con.cursor()
	cur.execute("SELECT ip,port,lastcheck FROM  acisi_http_proxy ORDER BY lastcheck ASC LIMIT 1;")
	result=cur.fetchone()
	operationok=True
	cur.execute('UPDATE acisi_http_proxy SET lastcheck=\''+str(datetime.datetime.now())+'\' WHERE ip=\''+str(result[0])+'\' AND port='+str(result[1])+';')
	con.commit()
	webresult=(str(ProxyRequestPage('http://acisi.ru/api/?action=webinfo',str(result[0]),str(result[1])).data,'utf-8'))
	json_result=json.loads(webresult)[1]['AcisiProject']
	if json_result=='READY':
		isactive=True
	cur.close
	con.close
except:
	isactive=False
if operationok:
	con=DatabaseConnection()
	cur=con.cursor()
	cur.execute('UPDATE acisi_http_proxy SET active='+str(isactive)+', lastcheck=\''+str(datetime.datetime.now())+'\' WHERE ip=\''+str(result[0])+'\' AND port='+str(result[1])+';')
	con.commit()
	cur.close()
	con.close()
	print (str(result)+' '+str(isactive))