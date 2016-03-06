import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests
import re

url = 'https://foursquare.com/v/bida-manda-laotian-restaurant-and-bar/4ee404309911944900b07ad5'

def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext


google_obj = {}
jsonArray = []
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
for e in soup.findAll('br'):
    e.extract()	
# fetch image
imgUl = soup.find("ul", class_="photos")
imgLi = imgUl.find("li", class_="photo photoWithContent")
imgSrc = imgLi.find("img")['src']
print imgSrc

header = soup.find("ul", id="tipsList")
info = header.find_all("li", class_="tip tipWithLogging")
cnt = 0
for review in info:
	wrap = review.find("div", class_="tipContents").find("p", class_="tipText")
	#print wrap
	if wrap is not None:
		text = re.sub('<[^>]*>', '', str(wrap))
		jsonArray.append({"scale":"", "review":text})
		cnt = cnt + 1
		print text
		print '.....................'
	if cnt == 5:
		break

google_obj['reviews'] = jsonArray
print google_obj

