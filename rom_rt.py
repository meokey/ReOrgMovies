#ReOrgMovies Module: Rotten Tomatoes

import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as matcher

from rom_common import *

def rt_grabinfo(title,year):
	"""search_rt(title)
return {'title':p[bestguess][0].strip(),'url':p[bestguess][2].strip(),'Rotten Tomatoes Score':p[bestguess][3].strip()} or None
"""

	if not title:
		return None
	#print (title)
	year = tidyyear(year)
	
	baseurl =  "http://www.rottentomatoes.com/search/?search="
	affix = title.replace(' ','%20')
		
	readHtml=readurl(baseurl,affix)
	with codecs.open("tt2527336.rt_search.db", 'w', 'utf-8') as f:
		f.write(str(readHtml))
	#with codecs.open("tt2527336.rt_search.db", 'r', 'utf-8') as f:
	#	readHtml = f.read()
	soup = BeautifulSoup(readHtml, "lxml")
	#print (soup)
	
	try:
		a = soup.find('div',class_="col col-left-center col-full-xs").find('script').text
	except:
		return None

	p = re.search('"movies"\:\[(.*)\],"tvCount"',a)
	if p:
		a = p.group(1)
	p = re.findall('"name"\:"([^"]*)","year"\:(\d{4}),"url"\:"([^"]*)".*"meterScore"\:(\d+)',a)
	if p:
		similarity = 0
		bestguess = None
		for i in range(len(p)):
			y = p[i][1].strip()
			if year:
				if year != y:
					continue
			t = p[i][0].strip()
			s = matcher(None,t,title).ratio()*100
			if s > similarity:
				similarity = s
				bestguess = i
		if bestguess != None:
			return {'title':p[bestguess][0].strip(),'url':p[bestguess][2].strip(),'Rotten Tomatoes Score':p[bestguess][3].strip()}	
		

	return None
	
#def rt_grabinfo(rt):
#	"""rt_grabinfo(rt)
#return {"Modified Date":rt_bydate,"Rotten Tomatoes Score":rt_score,"Audience Score":audience_score} or None
#"""
#
#	#print ("rt info:",rt)
#	if not rt:
#		return None
#	if not rt['url'].strip():
#		return None
#	#print ("rt url=",rt['url'].strip())
#
#	baseurl = 'http://www.rt.com'
#	readHtml=readurl(baseurl,rt['url'])
#	with codecs.open("tt"+rt['rtno']+".rt.db", 'w', 'utf-8') as f:
#		f.write(str(readHtml))
#	#with codecs.open("tt"+rt['rtno']+".rt.db", 'r', 'utf-8') as f:
#	#	readHtml = f.read()
#
#	soup = BeautifulSoup(readHtml, "lxml")
#	if soup == None:
#		return None
#
#	#print (soup)
#
#	movie = {}
#	movie['title'] = rt['title']
#	del rt['title']
#	try:
#		rt['RT Score'] = soup.find('span',attrs={'itemprop':'ratingValue'}).text.strip()
#	except:
#		pass
#	try:
#		movie['Meta Score']= soup.find('div',{'class',re.compile('metacriticScore.*')}).find('span').text.strip()
#	except:
#		pass
#	try:
#		movie['duration'] = soup.find('time',{'itemprop':'duration'}).text.strip()
#	except:
#		pass
#	try:
#		movie['datePublished'] = soup.find('meta',{'itemprop':"datePublished"})['content'].strip()
#	except:
#		pass
#	try:
#		movie['poster url'] = soup.find('div',{'class':'poster'}).find('img')['src'].strip()
#	except:
#		pass
#	try:
#		movie['summary'] = soup.find('div',{'class':'summary_text'}).text.strip()
#	except:
#		pass
#
#	roles = {('Director','director','span'),('Writers','creator','span'),('Stars','actors','span')}	
#	people_soup = soup.findAll('div',class_='credit_summary_item')
#	if people_soup:
#		for role,prop,tag in roles:
#			movie[role] = []
#			for i in range(len(people_soup)):
#				pp = people_soup[i].findAll(tag,{'itemprop':prop})
#				if pp:
#					for j in range(len(pp)):
#						p = pp[j].findAll('span',{'itemprop':'name'})
#						if p:
#							for k in range(len(p)):
#								movie[role].append(p[k].text)
#			#print (movie[role])
#
#	genres_soup = soup.find('div',{'itemprop':"genre"}).findAll('a')
#	if genres_soup:
#		movie['Genres'] = []
#		for i in range(len(genres_soup)):
#			movie['Genres'].append(genres_soup[i].text.strip())
#
#	blocks = {('Country','a'),('Language','a'),('Also Known As','#2'),('Filming Locations','a'),('Production Co','a'),('Sound Mix','a'),('Color','a'),('Aspect Ratio','#2')}
#	block_soup = soup.findAll('div',class_='txt-block')
#	if block_soup:
#		for block,tag in blocks:
#			for i in range(len(block_soup)):
#				p = block_soup[i].find('h4')
#				if p:
#					if p.text == block+":":
#						if tag[0] == '#':
#							movie[block] = block_soup[i].contents[int(tag[1:])].strip()
#							continue
#
#						p = block_soup[i].findAll(tag)
#						if p:
#							if len(p) == 1:
#								movie[block] = p[0].text.strip()
#							elif len(p) > 1:
#								movie[block] = []
#								for j in range(len(p)):
#									if p[j].text.strip().lower()  != 'see more':
#										movie[block].append(p[j].text.strip())
#							else:
#								pass	
#
#	movie['RT']=rt
#	#print (movie)
#	return movie
#	
