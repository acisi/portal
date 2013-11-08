#!/usr/bin/python3
# -*- coding: utf-8 -*-

from BaseFunctions import *
from WebElements import *
import os

script_path=os.path.dirname( __file__ )
keywords=ReadLines(script_path+"/../settings/ProxyKeywords.data")
urls=[]
for request in keywords:
	if request!='':
		#print(GetRamblerUrlsByKeyword(request))
		urls.extend(GetRamblerUrlsByKeyword(request))
print (urls)

