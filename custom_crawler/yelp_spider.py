import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests

url = 'http://www.yelp.com/biz/guasaca-raleigh'

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

google_obj = {}
reviewArr = []
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
#soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
#nonBreakSpace = u'\xa0'
#soup = soup.strip(nonBreakSpace)
for e in soup.findAll('br'):
    e.extract()	
#print soup

header = soup.find("ul", class_="ylist-bordered")
info = header.find_all("li", recursive=False)
name = soup.find("h1", class_="biz-page-title").contents
print "name: ", name
cnt = 0;
for review in info:
	wrap = review.find("div", class_="review-wrapper").find("p", {"itemprop":"description"})
	if wrap is not None: 
		text = removeNonAscii(wrap.contents[0])
		#nonBreakSpace = u'\xa0'
		#text = text.strip(nonBreakSpace)
		scale = review.find("div", class_="review-wrapper").find("meta", {"itemprop":"ratingValue"})['content']
		reviewArr.append({"scale":scale, "review":text})
		cnt = cnt + 1
		#print removeNonAscii(text)
	if cnt == 5:
		break
	

google_obj['reviews'] = reviewArr
print google_obj
#text = re.sub('[/\u00a0]*', '', text)

