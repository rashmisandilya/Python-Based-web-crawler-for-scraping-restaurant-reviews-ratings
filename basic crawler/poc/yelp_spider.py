import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests

url = 'http://www.yelp.com/biz/guasaca-raleigh'

google_obj = {}
jsonArray = []
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
google_obj['reviews'] = jsonArray
print google_obj
