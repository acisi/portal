#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from BaseFunctions import ReadLines
from BaseFunctions import RandomString
from portal_pages import ProxyProjectInfo
from WebElements import GetRandomActiveProxy
from WebElements import IsEmailActiveMailRU

import json

def PortalPages(request):
	html='<html>\
	<head>\
	<head>\
	<body>\
	'+ProxyProjectInfo()+'\
	</body>\
	</html>'
	return HttpResponse(html)

def api(request):
	html=json.dumps(['ApiResponse', {'status':'error'}])
	try:
		action=request.GET['action']
	except:
		action=''
	# Check WEB connection
	if action=="webinfo":
		html=json.dumps([{'result':'ok'},{'AcisiProject':'READY'}])
	# Get random active http proxy
	elif action=='randomproxy':
		html=GetRandomActiveProxy()
	elif action == 'mailrucheck':
		try:
			email=request.GET['email']
		except:
			email=""
		if email!="":
			res=IsEmailActiveMailRU(email)
			html=json.dumps([{'result':'ok'},{'active':str(res[0])},{'email':email},{'name':str(res[1])}])+str(res[2])
	return HttpResponse(html)