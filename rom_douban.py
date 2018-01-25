#ReOrgMovies Module: Douban

import re
#import codecs
#import urllib.request
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as matcher

from rom_common import *

def douban_grabinfo(imdbno,year=''):
	"""douban_grabinfo(imdbno,year='')
return {'Title CN':title,'Douban Score':douban_score,'Douban URL':url} or None
"""
	imdbno = tidyimdb(imdbno)
	if imdbno == '':
		return None
	year = tidyyear(year)
	
	baseurl =  "http://m.douban.com/search/?query=tt"
		
	readHtml=readurl(baseurl,imdbno)
	#with codecs.open("tt"+imdbno+".douban_search.db", 'w', 'utf-8') as f:
	#	f.write(str(readHtml))
	#with codecs.open("tt"+imdbno+".douban_search.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()
	soup = BeautifulSoup(readHtml, "lxml")
	#print (soup)
	
	try:
		a = soup.find('ul',class_='search_results_subjects').find('li')
	except:
		return None
	
	try:
		title = a.find('span',class_="subject-title").text.strip()
		douban_score = a.find('p',class_="rating").text.strip()
	except:
		return None
	try:
		douban_score = a.find('p',class_="rating").text.strip()
	except:
		douban_score = ''
	try:
		url = a.find('a')['href']
	except:
		url = ''

	return {'Title CN':title,'Douban Score':douban_score,'Douban URL':url}


