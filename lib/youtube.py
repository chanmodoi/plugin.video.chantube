import xbmcaddon
import thread, threading
import urllib, urllib2
import datetime, time
import xbmc
import logging
from bs4 import BeautifulSoup
import requests
import html5lib

class Item:
	def __init__(self, link, title, img):
		self.link = link
		self.title = title
		self.img = img
def getListVideos(url):
	r = requests.get(url+"videos")
	html = r.text	
	#xbmc.log(html.encode("utf-8"))
	soup = BeautifulSoup(html)
	list_a = soup.findAll('a')
	list_links=[]
	for a in list_a:
		a_href = a.get("href")
		a_title = a.get("title")		
		if (a_href!=None) and (a_href.startswith("/watch?v=")) and (a_title!=None):
			a_img = "https://i.ytimg.com/vi/"+a_href[9:]+"/mqdefault.jpg"
			list_links.append(Item("https://www.youtube.com" + a_href, a_title, a_img))
	return list_links
def getLinkFromKeepVid(link):
	r = requests.get("http://keepvid.com/" + '?' + urllib.urlencode({"url":link}))
	html = r.text
	soup = BeautifulSoup(html, "html5lib")
	
	list_a = soup.findAll('a', attrs = {"class":"l"})
	#xbmc.log(list_a.text)
	links=[]
	for a in list_a:
		links.append(a.get("href"))
	return links	