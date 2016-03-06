# Python crawler to fetch the reviews and ratings from yelp, trip advisor and four square
# for restaurant reviews
# Author: sbalakr2

import urllib2
from bs4 import BeautifulSoup
import requests
from os import listdir
from os import getcwd
import json
import csv
import re
import tinys3

# Method to remove symbols in the restaurant reviews
def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

#Method to fetch the restaurant reviews from trip advisor
def getReviewsForTripAdvisor(soup):
	reviewArr = []
	header = soup.find("div", id="REVIEWS")
	info = header.find_all("div", class_="reviewSelector")
	cnt = 0
	for review in info:
		#print "id..",review['id']
		wrap = review.find("div", class_="wrap")
		if wrap is not None:
			scale = wrap.find("img")['alt'].split(' ')[0]
			text = wrap.find("p", class_="partial_entry").contents[0].strip()
			text = re.sub('<span class="partnerRvw">.*</span>', '', removeNonAscii(text))
			text = re.sub('<img>.*</img>', '', text)
			reviewArr.append({"scale":scale, "review":text})
			cnt = cnt + 1
		if cnt == 5:
			break
	return reviewArr

#Method to fetch the restaurant reviews from four square
def getReviewsForFourSquare(soup):
	reviewArr = []
	header = soup.find("ul", id="tipsList")
	info = header.find_all("li", class_="tip tipWithLogging")
	cnt = 0
	for review in info:
		wrap = review.find("div", class_="tipContents").find("p", class_="tipText")
		if wrap is not None:
			text = removeNonAscii(re.sub('<[^>]*>', '', str(wrap))).strip()
			reviewArr.append({"scale":"", "review":text})
			cnt = cnt + 1
		if cnt == 5:
			break
	return reviewArr

#Method to fetch the restaurant reviews from yelp.com
def getReviewsForYelp(soup):
	reviewArr = []
	header = soup.find("ul", class_="ylist-bordered")
	info = header.find_all("li", recursive=False)
	cnt = 0
	for review in info:
		wrap = review.find("div", class_="review-wrapper").find("p", {"itemprop":"description"})
		if wrap is not None: 
			text = removeNonAscii(wrap.contents[0]).strip()
			scale = review.find("div", class_="review-wrapper").find("meta", {"itemprop":"ratingValue"})['content']
			reviewArr.append({"scale":scale, "review":text})
			cnt = cnt + 1
		if cnt == 5:
			break
	#print reviewArr
	return reviewArr

# Method to fetch the url of the photo of the restaurant
# One image is enough, hence fetching it from four square
def getPhotoUrlFromFourSquare(soup):
	imgUl = soup.find("ul", class_="photos")
	imgLi = imgUl.find("li", class_="photo photoWithContent")
	imgSrc = imgLi.find("img")['src']
	return imgSrc

# Method to crawl the three web pages in to get the overall rating
# and number of reviews for each restaurant
def crawlpage(restaurant_id, restaurant_name, url_list):
	count = 0
	finalJson = {}
	jsonData = {}
	data = {}
	yelp_obj = {}
	foursq_obj = {}
	trip_obj = {}
	for weburl in url_list:
		print weburl	
		page = requests.get(weburl)
		soup = BeautifulSoup(page.text,'html.parser')
		for e in soup.findAll('br'):
    			e.extract()	

		if count == 0:
			print "yelp"
			header = soup.find("div", class_="biz-page-header-left")
			info = header.find("div", class_="biz-rating")
			overall_rating = info.find("i", class_="star-img")['title'].split(' ')[0]
			total_reviews = info.find("span", class_="review-count").find("span").contents[0]
			yelp_obj['rating'] = overall_rating
			yelp_obj['count'] = total_reviews
			yelp_obj['reviews'] = getReviewsForYelp(soup)
			yelp_obj['url'] = weburl

		elif count == 1:
			print "tripadvisor"
			info = soup.find("div", class_="rs rating")
			overall_rating = info.find("img")['content']
			total_reviews = info.find("a")['content']
			trip_obj['rating'] = overall_rating
			trip_obj['count'] = total_reviews
			trip_obj['reviews'] = getReviewsForTripAdvisor(soup)
			trip_obj['url'] = weburl

		elif count == 2:
			print "foursquare"
			header = soup.find("div", class_="attrBar")
			info = header.find("div", class_="leftColumn")
			overall_rating = info.find("span", {"itemprop":"ratingValue"}).contents[0]
			total_reviews = info.find("span", {"itemprop":"ratingCount"}).contents[0]
			foursq_obj['rating'] = overall_rating
			foursq_obj['count'] = total_reviews
			foursq_obj['reviews'] = getReviewsForFourSquare(soup)
			foursq_obj['url'] = weburl

		count = count + 1

	data['yelp'] = yelp_obj
	data['foursquare'] = foursq_obj
	data['tripadvisor'] = trip_obj
	jsonData['name'] = restaurant_name
	jsonData['photo_url'] = getPhotoUrlFromFourSquare(soup) # out of for loop, soup has foursquare data
	jsonData['data'] = data
	finalJson[restaurant_id] = jsonData
	return finalJson

# Method to upload the given file to Amazon S3 Bucket
def uploadJsonToServer():
	print 'in upload'
	# Connection uses AWS Access Key and Secret Key which are passed below
	# if changes to the keys, update here
	accessKey = 'AKIAITSQQ4I64PHL6PKQ'
	secretKey = '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'
	conn = tinys3.Connection(accessKey, secretKey,tls=True)
	f = open('restaurants.json','rb')
	conn.upload('restaurants.json',f,'restoscrapper')

# Method to fetch restaurant name from the url
def fetchNameFromUrl(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text,'html.parser')
	name = soup.find("h1", class_="biz-page-title").contents[0]
	print name.strip()
	return name.strip()

# Initially called method to initiate the crawler and
# create the json file containing the ratings and reviews
# and finally upload the json in the cloud Amazon AWS S3 Bucket
def crawlCsvAndCreateJsonFile(fileName, jsonfile):
	ifile  = open(fileName, "rb")
	jsonFile = open(jsonfile,"w")
	reader = csv.reader(ifile)
	rownum = 0
	mainJson = {}
	jsonArray = []
	for row in reader:
		#print row
		if rownum == 0:
			header = row
		else:
			url_list = []
			rid = row[0]
			name = fetchNameFromUrl(row[1])
			url_list.append(row[1])
			url_list.append(row[2])
			url_list.append(row[3])
		    	json_data = crawlpage(rid, name, url_list)
			jsonArray.append(json_data)
		rownum += 1
	mainJson['restaurants'] = jsonArray
	#print mainJson
	jsondata = json.dumps(mainJson)
	jsonFile.write(jsondata)
	ifile.close()
	jsonFile.close()
	uploadJsonToServer()

crawlCsvAndCreateJsonFile('sample-restaurants-link.csv', 'restaurants.json');
