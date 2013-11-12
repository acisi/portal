#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import string

def RandomString(length=7):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

def ReadLines(filename):
	f = open(filename,'r')
	linearray=[]
	for line in f.readlines():
		linearray.append(line.replace('\n',''))
	f.close()
	return linearray

def WriteLines(filename,lines):
	f=open(filename, 'w')
	f.write(lines)
	f.close()
	return lines

def CheckIP(_ip):
	ip=_ip.split('.')
	try:
		o1=int(ip[0])
		o2=int(ip[1])
		o3=int(ip[2])
		o4=int(ip[3])
		result=str(o1)+"."+str(o2)+"."+str(o3)+"."+str(o4)
	except:
		result="0.0.0.0"
	if result!="0.0.0.0":
		if o1==127:
			result="0.0.0.0"
		if o1==10:
			result="0.0.0.0"
		if o1==172 and o2>=16 and o2<=31:
			result="0.0.0.0"
		if o1==192 and o2==168:
			result="0.0.0.0"
		if o1==169 and o2==254:
			result="0.0.0.0"
		if o1>255 or o2>255 or o3>255 or o4>255:
			result="0.0.0.0"
		if o1<0 or o2<0 or o3<0 or o4<0:
			result="0.0.0.0"
	if result!='0.0.0.0':
		validip=result
	else:
		validip='0.0.0.0'
	return validip