import sys, datetime
import re
import codecs
import urllib.request
from selenium import webdriver	#sudo pip install selenium, some issue exist, cannot use
from bs4 import BeautifulSoup	#sudo pip install beautifulsoup4
from difflib import SequenceMatcher as matcher

def tidyyear(year):
	"""return str(year) or '' """

	if type(year) != str:
		try:
			year = str(year)
		except:
			return ''
	p = re.search('(\d{4})',year)
	if p:
		year = int(p.group(1).strip())
		if year >= 1915 and year <= datetime.date.today().year:
			return str(year)
	return ''

def tidyimdb(imdb):
	""" return p.group(2).strip() or '' """
	if type(imdb) != str:
                try:
                        imdb = str(imdb)
                except:
                        return ''
	p = re.search('(tt)?(\d{7})',imdb)
	if p:
		return p.group(2).strip()
	return ''

def ishan(text):
    """ sample: ishan('一') == False, ishan('我&&你') == True	"""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def utf8asc(text):
	if ishan(text):
		return urllib.parse.quote(text.encode('utf8'), safe='')
	else:
		return text

def readurl(baseurl,affix,rendering=False):
	""" return HTML, HTML = HTML.decode(hcharset), or None
"""
	if baseurl[:4] != 'http':
		return None
	affix=utf8asc(affix)
	hurl = urllib.request.urlopen(baseurl+affix)
	if hurl == None:
		return None
	HTML = hurl.read()
	hcharset = hurl.headers.get_content_charset()
	hurl.close()

	if hcharset:
		HTML = HTML.decode(hcharset)
	#if rendering:
	#	browser = webdriver.PhantomJS()	#selenium for PhantomJS
	#	browser.get(HTML)
	#	HTML = browser.page_source	#fetch HTML source code after rendering
	#	browser.quit()

	return HTML
