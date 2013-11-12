#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from BaseFunctions import ReadLines
import json

def PortalPages(request):
	html='<html>\
	<head>\
	<head>\
	<body>\
	</body>\
	</html>'
	return HttpResponse(html)

def api(request):
	html=json.dumps(['ApiResponse', {'status':'error'}])
	try:
		action=request.GET['action']
	except:
		action=''
	if action=="webinfo":
		html=json.dumps([{'result':'ok'},{'AcisiProject':'READY'}])
#	elif n== 1 or n == 9 or n == 4:
#		print "n is a perfect square\n"
#	elif n == 2:
#		print "n is an even number\n"
	return HttpResponse(html)