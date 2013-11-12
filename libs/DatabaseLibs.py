#!/usr/bin/python3
import psycopg2
import os
from BaseFunctions import ReadLines

script_path=os.path.dirname( __file__ )
DataBaseSettings=ReadLines(script_path+"/database_settings.conf")

def DatabaseConnection():
	conn_string = "host='"+DataBaseSettings[3]+"' dbname='"+DataBaseSettings[0]+"' user='"+DataBaseSettings[1]+"' password='"+DataBaseSettings[2]+"'"
	conn=psycopg2.connect(conn_string)
	return conn
