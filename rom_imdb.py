#ReOrgMovies Module: IMDB

import re
import codecs
import urllib.request
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as matcher

from rom_common import *

def search_imdb(title,year):
	"""search_imdb(title)
return {"title":ftitle,"url":furl,"imdbno":fimdbno}) or None
"""

	if not title:
		return None
	#print (title)
	year = tidyyear(year)
	
	baseurl =  "http://www.imdb.com/search/title?title_type=feature&title="
	affix = title.replace(' ','+')
	if year != '':
		affix = affix+"&release_date="+year+","+year
		
	readHtml=readurl(baseurl,affix)
	with codecs.open("tt2527336.imdb_search.db", 'w', 'utf-8') as f:
		f.write(str(readHtml))
	#with codecs.open("tt2527336.imdb_search.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()
	soup = BeautifulSoup(readHtml, "lxml")
	#print (soup)
	
	try:
		a = soup.findAll('div',class_="lister-item-content")
	except:
		return None

	similarity = 0
	bestguess = None
	for i in range(len(a)):
		f = a[i].find('h3').find('a').text.strip()
		url =''
		imdbno=''
		p = re.search('(\/title\/tt(\d{7})\/)',a[i].find('h3').find('a')['href'].strip())
		if p:
			url = p.group(1).strip()
			imdbno = p.group(2).strip()
		s = matcher(None,f,title).ratio()*100
		if s > similarity:
			similarity = s
			bestguess = i
			ftitle = f
			furl = url
			fimdbno = imdbno
			#print (ftitle,bestguess)
	if bestguess != None:
		return {"title":ftitle,"url":furl,"imdbno":fimdbno}
	else:
		return None
	
def imdb_grabinfo(imdb):
	"""imdb_grabinfo(imdb)
return {"Modified Date":rt_bydate,"Rotten Tomatoes Score":rt_score,"Audience Score":audience_score} or None
"""

	#print ("imdb info:",imdb)
	if not imdb:
		return None
	if not imdb['url'].strip():
		return None
	#print ("imdb url=",imdb['url'].strip())

	baseurl = 'http://www.imdb.com'
	readHtml=readurl(baseurl,imdb['url'])
	with codecs.open("tt"+imdb['imdbno']+".imdb.db", 'w', 'utf-8') as f:
		f.write(str(readHtml))
	#with codecs.open("tt"+imdb['imdbno']+".imdb.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()

	soup = BeautifulSoup(readHtml, "lxml")
	if soup == None:
		return None

	#print (soup)

	movie = {}
	movie['title'] = imdb['title']
	del imdb['title']
	try:
		imdb['IMDB Score'] = soup.find('span',attrs={'itemprop':'ratingValue'}).text.strip()
	except:
		pass
	try:
		movie['Meta Score']= soup.find('div',{'class',re.compile('metacriticScore.*')}).find('span').text.strip()
	except:
		pass
	try:
		movie['duration'] = soup.find('time',{'itemprop':'duration'}).text.strip()
	except:
		pass
	try:
		movie['datePublished'] = soup.find('meta',{'itemprop':"datePublished"})['content'].strip()
	except:
		pass
	try:
		movie['poster url'] = soup.find('div',{'class':'poster'}).find('img')['src'].strip()
	except:
		pass
	try:
		movie['summary'] = soup.find('div',{'class':'summary_text'}).text.strip()
	except:
		pass

	roles = {('Director','director','span'),('Writers','creator','span'),('Stars','actors','span')}	
	people_soup = soup.findAll('div',class_='credit_summary_item')
	if people_soup:
		for role,prop,tag in roles:
			movie[role] = []
			for i in range(len(people_soup)):
				pp = people_soup[i].findAll(tag,{'itemprop':prop})
				if pp:
					for j in range(len(pp)):
						p = pp[j].findAll('span',{'itemprop':'name'})
						if p:
							for k in range(len(p)):
								movie[role].append(p[k].text)
			#print (movie[role])

	genres_soup = soup.find('div',{'itemprop':"genre"}).findAll('a')
	if genres_soup:
		movie['Genres'] = []
		for i in range(len(genres_soup)):
			movie['Genres'].append(genres_soup[i].text.strip())

	blocks = {('Country','a'),('Language','a'),('Also Known As','#2'),('Filming Locations','a'),('Production Co','a'),('Sound Mix','a'),('Color','a'),('Aspect Ratio','#2')}
	block_soup = soup.findAll('div',class_='txt-block')
	if block_soup:
		for block,tag in blocks:
			for i in range(len(block_soup)):
				p = block_soup[i].find('h4')
				if p:
					if p.text == block+":":
						if tag[0] == '#':
							movie[block] = block_soup[i].contents[int(tag[1:])].strip()
							continue

						p = block_soup[i].findAll(tag)
						if p:
							if len(p) == 1:
								movie[block] = p[0].text.strip()
							elif len(p) > 1:
								movie[block] = []
								for j in range(len(p)):
									if p[j].text.strip().lower()  != 'see more':
										movie[block].append(p[j].text.strip())
							else:
								pass	

	movie['IMDB']=imdb
	#print (movie)
	return movie
	
