import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests

articleurl = 'http://www.yelp.com/search?find_desc=kabob+and+curry&find_loc=Cary%2C+NC&ns=1'

def crawlpage(articleurl):
	page = requests.get(articleurl)
	soup = BeautifulSoup(page.text,'html.parser')	
	test = soup.find("div", class_="search-results-content")
	cnt = 0
	for eachul in test.find_all("ul", recursive=False):
		contents = eachul.contents
		#length = len(contents)
		#print length
		print contents
		for content in contents:
			print content
			print len(content)
			break
		#cnt = cnt + 1

	#print "cnt..",cnt
	#print test.find("ul").next_sibling


crawlpage(articleurl)
