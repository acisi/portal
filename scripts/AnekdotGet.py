#!/usr/bin/python3
# -*- coding: utf-8 -*-
######################################################################################
#                                                                                    #
# Парсер для сайта Anekdot.ru                                                        #
#                                                                                    #
######################################################################################

import os
import json
import datetime
from DatabaseLibs import DatabaseConnection
from WebElements import RequestPage

script_path=os.path.dirname( __file__ )

text=str(RequestPage('http://pda.anekdot.ru/anekdots/random?show=full'),'cp1251')
main_data=text.split('<h1>Анекдоты / Случайные</h1>')[1].split('<div id="yandex_ad">')[0]
a1=main_data.split('<div class="a_mt10 a_mb10">')[0]
a2=main_data.split('</div>')[1]
text_to_analyse=a1+a2
con=DatabaseConnection()
cur=con.cursor()
for data in text_to_analyse.split('</p>'):
	if data.count('<div class')==0:
		data=data.replace('<p>','')
		data=data.replace('<br />','\n')
		data=data.replace('&quot;','"')
		#print (data)
		try:
			cur.execute("INSERT INTO acisi_anekdot (text, postdate) VALUES (%s, %s)", (data, datetime.datetime.now()))
			con.commit()
		except:
			#print ("Except")
			con.commit()
		#print ('======================')
cur.close()
con.close()