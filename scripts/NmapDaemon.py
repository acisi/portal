#!/usr/bin/python3
# -*- coding: utf-8 -*-
##################################################################
#                                                                #
# Автономный Nmap сканер для поиска потенциальных http-proxy     #
# При обнаружении создает запись в базе данных http_proxy.sqlite #
#                                                                #
##################################################################
import sqlite3
import os
import subprocess

script_path=os.path.dirname( __file__ )
con = sqlite3.connect(script_path+"/../data/uniq_ip.sqlite")
cur = con.cursor()
try:
	cur.execute('SELECT id,ip FROM uniq_ip WHERE c1=\'False\' ORDER BY RANDOM() LIMIT 1')
	res=cur.fetchone()
	id_=res[0]
	ip_=res[1]
except:
	id_=0
	ip_='0.0.0.0'
updated=False
if ip_!='0.0.0.0':
	try:
		cur.execute('UPDATE uniq_ip SET c1=\'True\' WHERE id='+str(id_)+'')
		con.commit()
		stage_2=True
	except:
		stage_2=False
	if stage_2:
		nmapresults=subprocess.check_output(["nmap", "-sV", "-Pn", str(ip_)]).decode("utf-8")
		for result in nmapresults.split('\n'):
			try:
				proxy_port=result.split(' ')
				proxy_port=list(filter(None,proxy_port))
				if proxy_port[1]=='open':
					if proxy_port[2]=='http-proxy':
						port=proxy_port[0].split('/')[0]
						con_2 = sqlite3.connect(script_path+"/../data/http_proxy.sqlite")
						cur_2 = con_2.cursor()
						cur_2.execute('insert into http_proxy (ip,port) values (\''+ip_+'\','+str(port)+');')
						con_2.commit()
						cur_2.close()
						con_2.close()
				updated=True
			except:
				proxy_port=0
if updated:
	cur.execute('UPDATE uniq_ip SET c2=\'True\' WHERE id='+str(id_)+'')
	con.commit()
cur.close()
con.close()