#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from BaseFunctions import ReadLines
import json

def ProxyProjectInfo():
	html='<p>Only API :(</p>\
		<p>You can contact me at: acisi82@mail.ru</p>'
	return html