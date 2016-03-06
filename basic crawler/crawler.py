import urllib2
from bs4 import BeautifulSoup
import requests
from os import listdir
from os import getcwd
import json
import csv

def crawlpage(restaurant_id, restaurant_name, url_list):
	count = 0
	finalJson = {}
	jsonData = {}
	data = {}
	yelp_obj = {}
	google_obj = {}
	trip_obj = {}
	for weburl in url_list:
		print weburl	
		page = requests.get(weburl)
		soup = BeautifulSoup(page.text,'html.parser')

		if count == 0:
			print "yelp"
			header = soup.find("div", class_="biz-page-header-left")
			info = header.find("div", class_="biz-rating")
			overall_rating = info.find("i", class_="star-img")['title'].split(' ')[0]
			total_reviews = info.find("span", class_="review-count").find("span").contents[0]
			print overall_rating
			print total_reviews
			yelp_obj['rating'] = overall_rating
			yelp_obj['count'] = total_reviews
			yelp_obj['reviews'] = []

		elif count == 1:
			print "tripadvisor"
			info = soup.find("div", class_="rs rating")
			overall_rating = info.find("img")['content']
			total_reviews = info.find("a")['content']
			print overall_rating
			print total_reviews
			trip_obj['rating'] = overall_rating
			trip_obj['count'] = total_reviews
			trip_obj['reviews'] = []

		elif count == 2:
			print "googleratings"
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

		count = count + 1

	data['yelp'] = yelp_obj
	data['googleratings'] = google_obj
	data['tripadvisor'] = trip_obj
	jsonData['name'] = restaurant_name
	jsonData['data'] = data
	finalJson[restaurant_id] = jsonData
	return finalJson


def crawlCsvAndCreateJsonFile(fileName, jsonfile):
	ifile  = open(fileName, "rb")
	jsonFile = open(jsonfile,"w")
	reader = csv.reader(ifile, delimiter='\t')
	rownum = 0
	mainJson = {}
	jsonArray = []
	for row in reader:
		if rownum == 0:
			header = row
		else:
			url_list = []
			rid = row[0]
			name = row[1]
			url_list.append(row[2])
			url_list.append(row[3])
			url_list.append(row[4])
		    	json_data = crawlpage(rid, name, url_list)
			jsonArray.append(json_data)
		rownum += 1
	mainJson['restaurants'] = jsonArray
	print mainJson
	jsondata = json.dumps(mainJson)
	jsonFile.write(jsondata)
	ifile.close()
	jsonFile.close()

crawlCsvAndCreateJsonFile('test.csv', 'restaurants.json');
