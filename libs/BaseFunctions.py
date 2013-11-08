#!/usr/bin/python3
# -*- coding: utf-8 -*-

def ReadLines(filename):
	f = open(filename,'r',encoding='utf8')
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