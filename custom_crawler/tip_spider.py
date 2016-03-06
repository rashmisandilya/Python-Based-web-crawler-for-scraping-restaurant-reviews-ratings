import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests
import re

url = 'http://www.tripadvisor.com/Restaurant_Review-g49463-d3471247-Reviews-Bida_Manda-Raleigh_North_Carolina.html'

def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext


google_obj = {}
reviewArr = []
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
for e in soup.findAll('br'):
    e.extract()	

header = soup.find("div", id="REVIEWS")
info = header.find_all("div", class_="reviewSelector")
cnt = 0
for review in info:
	wrap = review.find("div", class_="wrap")
	#print wrap
	if wrap is not None:
		scale = wrap.find("img")['alt'].split(' ')[0]
		text = wrap.find("p", class_="partial_entry").contents[0]
		text = re.sub('<span class="partnerRvw">.*</span>', '', str(text))
		text = re.sub('<img>.*</img>', '', text)
		reviewArr.append({"scale":scale, "review":text})
		cnt = cnt + 1
		print text, '\n\n'
		print '...........'
	if cnt == 5:
		break
	
google_obj['reviews'] = reviewArr
#print google_obj

