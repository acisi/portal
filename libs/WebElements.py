#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib3
from urllib.request import quote

def GetRamblerUrlsByKeyword(keyword):
	result=[]
	http = urllib3.PoolManager()
	request=""
	spliter=""
	for item in keyword.split(" "):
		request=request+spliter+quote(item)
		spliter="+"
	res = http.request('GET', 'http://nova.rambler.ru/search?utm_source=nhp&query='+request)
	if res.status==200:
		for tmp_link in str(res.data).split('<li class="b-serp__list_item">')[1:]:
			try:
				link=tmp_link.split('<p class="b-serp__list_item_snippet">')[0].split('href="')[1].split('"')[0]
			except:
				link=''
			if link!='':
				result.append(link)
	return result
