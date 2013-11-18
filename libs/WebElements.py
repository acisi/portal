#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib3
import httplib2
import pycurl
import tempfile
import io
import os
from BaseFunctions import RandomString
from urllib.request import quote
from DatabaseLibs import DatabaseConnection

def GetBrowserHeaders():
	Headers=['User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0',\
	'Accept:text/html',\
	'Accept-Language:en-US,en;q=0.5',\
	'Connection:keep-alive']
	return Headers

class WebElements:
	temp_dir=tempfile.gettempdir()
	cookie=temp_dir+"/"+RandomString()+'.cookie'
	def __init__(self):
		self.Curl=pycurl.Curl()
	def SetPostRequest(self,post):
		self.Curl.setopt(self.Curl.POSTFIELDS,post)
	def HtmlContent(self,url):
		headbuf = io.StringIO()
		bodybuf = io.StringIO()
		try:
			self.Curl.setopt(self.Curl.URL,url)
			self.Curl.setopt(self.Curl.HEADERFUNCTION, headbuf.write)
			self.Curl.setopt(self.Curl.WRITEFUNCTION, bodybuf.write)
			self.Curl.setopt(self.Curl.COOKIEFILE, self.cookie)
			self.Curl.setopt(self.Curl.COOKIEJAR, self.cookie)
			self.Curl.setopt(self.Curl.HTTPHEADER,GetBrowserHeaders())
			self.Curl.setopt(self.Curl.CONNECTTIMEOUT, 15)
			self.Curl.setopt(self.Curl.TIMEOUT, 18)
			self.Curl.perform()
			Html=bodybuf.getvalue()
			Header=headbuf.getvalue()
		except:
			Html=''
			Header=''
		headbuf.close()
		bodybuf.close()
		return [Header,Html]

class WebMailRU(WebElements):
	def CheckEmailExist(self,email):
		exist=False
		e_mail=email.split('@')[0]
		e_mail_domain=email.split('@')[1]
		temp_dir=tempfile.gettempdir()
		cookie=temp_dir+"/"+RandomString()+'.cookie'
		h = httplib2.Http(cookie)
		resp, content = h.request("http://e.mail.ru/cgi-bin/signup?from=main", "GET")
		try:
			os.removedirs(cookie)
		except:
			tmp_error=''
		content=content.decode('utf-8','ignore')
		try:
			login_xid=content.split('<input autocomplete="off"')[1].split('value=""')[0].split('"')[1].split('"')[0]
			x_reg_id=content.split("'x_reg_id': '")[1].split("'")[0]
		except:
			login_xid=''
			x_reg_id=''
		self.SetPostRequest("RegistrationDomain="+e_mail_domain+"&Signup_utf8=1&"+login_xid+"="+e_mail+"&x_reg_id="+x_reg_id)
		result=str(self.HtmlContent('http://e.mail.ru/cgi-bin/checklogin')[1])
		if result=='EX_USEREXIST':
			exist=True
			#UpdateID=ElementsDB()
			#UpdateID.GetEmailID(email)
		return exist

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

def ProxyRequestPage(url,host,port):
	try:
		proxy = urllib3.proxy_from_url('http://'+host+':'+port+'/',timeout=20.0)
		html = proxy.request('GET', url)
	except:
		html=''
	return html

def GetRandomActiveProxy():
	try:
		con=DatabaseConnection()
		cur=con.cursor()
		cur.execute('SELECT ip,port FROM acisi_http_proxy WHERE active=\'True\' ORDER BY RANDOM() LIMIT 1;')
		result=cur.fetchone()
		cstring=result[0]+':'+str(result[1])
		cur.close()
		con.close()
	except:
		cstring='0.0.0.0:0'
	return cstring

def GetProxyList(items=1):
	proxylist=''
	con=DatabaseConnection()
	cur=con.cursor()
	cur.execute("SELECT ip,port FROM  acisi_http_proxy WHERE active=True ORDER BY lastcheck DESC LIMIT "+str(items)+";")
	result=cur.fetchall()
	delimeter=''
	for res in result:
		proxylist=proxylist+delimeter+res[0]+':'+str(res[1])
		delimeter='; '
	cur.close()
	con.close()
	return proxylist

def IsEmailActiveMailRU(email):
	temp=''
	web=WebMailRU()
	Exist=str(web.CheckEmailExist(email))
	result=[Exist,'None',temp]
	return result

