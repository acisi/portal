#!/usr/bin/python3
# -*- coding: utf-8 -*-
############################################################
#                                                          #
# Добавляем запись IP-адреса (Если он корректный).         #
# Часть ежедневно выполняемого скрипта по предварительному #
# сбору данных для проверки на открытые proxy.             #
#                                                          #
############################################################
#                                                          #
# Скрипт является частью проекта "acisi"                   #
# Автор: Черноусов Антон (acisi82@mail.ru)                 #
# WEB: http://www.acisi.ru                                 #
#                                                          #
############################################################
 
from BaseFunctions import ReadLines
from BaseFunctions import CheckIP
import os
import sqlite3

script_path=os.path.dirname( __file__ )
ip_address=ReadLines(script_path+"/../data/tmp/iplist.lst")
con = sqlite3.connect(script_path+"/../data/uniq_ip.sqlite")
cur = con.cursor()
for ip in ip_address:
    PublishIP=CheckIP(ip)
    if PublishIP!='0.0.0.0':
        try:
            cur.execute("insert into uniq_ip (ip) values ('"+PublishIP+"')")
            con.commit()
        except:
            con.commit()

cur.close()
con.close() 
