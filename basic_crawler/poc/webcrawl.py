import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests

articleurl = 'https://www.google.com/search?client=ubuntu&channel=fs&q=kabab+abd+curry&ie=utf-8&oe=utf-8#lrd=0x89acf58d91dc1a07:0x7b8b1d19952b99d5,1,,'
#url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=kabab+abd+curry&ie=utf-8&oe=utf-8#'
url = ''

def crawlpage(articleurl):
	google_obj = {}
	page = requests.get(url)
	soup = BeautifulSoup(page.text,'html.parser')	
	#print soup

	#header = soup.contents[1]#.find_all("div", recursive=False)
	#print header
	#print len(header)
	info = soup.find_all("div", class_="_o0d")[1]
	print info
	overall_rating = info.find("span", class_="_kgd").contents[0]
	total_reviews = info.find_all("span")[1].contents[0].split(' ')[1] 
	print overall_rating
	print total_reviews
	google_obj['rating'] = overall_rating
	google_obj['count'] = total_reviews
	google_obj['reviews'] = []
	print google_obj
 
crawlpage(articleurl)
