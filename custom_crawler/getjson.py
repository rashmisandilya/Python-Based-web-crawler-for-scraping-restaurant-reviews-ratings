import urllib2
#import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import requests
from os import listdir
from os import getcwd
import json

name = 'el cerro'
id = '1903824'
data = {}
data2 = {}
overall_rating = '4.5'
total_reviews = '79'

data['rating'] = overall_rating
data['count'] = total_reviews
data['reviews'] = []
data2['yelp'] = data
print data2


