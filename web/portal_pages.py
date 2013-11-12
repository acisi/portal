#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from BaseFunctions import ReadLines
import json

def ProxyProjectInfo():
	html='<p>Project proxy info:</p>'
	return html