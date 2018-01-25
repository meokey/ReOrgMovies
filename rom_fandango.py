#ReOrgMovies Module: Fandango

import re
import codecs
import urllib.request
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as matcher

from rom_common import *

def search_fandango(title):
	"""search_fandango(title)
return {"title":p[bestguess].find('h3').find('a').text.strip(),"url":p[bestguess].find('h3').find('a')['href'].strip()) or None
"""

	if not title:
		return None
	#print (title)
	
	baseurl =  "https://www.fandango.com/search?mode=movies&q="
	readHtml=readurl(baseurl,title.replace(' ','+'))
	with codecs.open("tt2527336.fandango_search.db", 'w', 'utf-8') as f:
		f.write(str(readHtml))
	#with codecs.open("tt2527336.fandango_search.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()
	soup = BeautifulSoup(readHtml, "lxml")
	#print (soup)

	try:
		a = soup.findAll('ul',class_="results-list")
	except:
		return None

	try:
		a = a[0].findAll('div',class_="results-detail")
	except:
		return None

	similarity = 0
	bestguess = None
	for i in range(len(a)):
		f = a[i].find('h3').find('a').text.strip()
		url = a[i].find('h3').find('a')['href'].strip()
		s = matcher(None,f,title).ratio()*100
		if s > similarity:
			similarity = s
			bestguess = i
			ftitle = f
			furl = url
			#print (ftitle,bestguess)
	if bestguess != None:
		return {"title":ftitle,"url":furl}
	else:
		return None
	
def rt_grabinfo(movie):
	"""rt_grabinfo(movie)
return {"Modified Date":rt_bydate,"Rotten Tomatoes Score":rt_score,"Audience Score":audience_score} or None
"""

	#print ("rt info:",movie)
	if not movie:
		return None
	#print ("rt url=",movie[2].strip())
	if not movie[2].strip():
		return None
		
	baseurl = 'https://www.rottentomatoes.com'
	readHtml=readurl(baseurl,movie[2].strip())
	#with codecs.open("tt2527336.rt.db", 'w', 'utf-8') as f:
	#	f.write(str(readHtml))
	#with codecs.open("tt2527336.rt.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()
	soup = BeautifulSoup(readHtml, "lxml")
	if soup:
		#print (soup)
		try:
			audience_score = soup.find('div',class_='audience-score meter').find('span').contents[0]
		except:
			audience_score = None
			
		try:
			rt_soup = soup.find('script',id="jsonLdSchema").contents[0]
		except:
			#rt_soup = None
			return None
			
		if rt_soup:
			p=re.search('"AggregateRating","ratingValue":(\d+),',rt_soup)
			rt_score = None
			if p:
				rt_score = p[1]+"%"
			p=re.search('"dateModified"\:"([^T]*)T',rt_soup)
			rt_bydate = None
			if p:
				rt_bydate = p[1]
				
			return {"Modified Date":rt_bydate,"Rotten Tomatoes Score":rt_score,"Audience Score":audience_score}
		else:
			return None
		
	else:
		return None
	
