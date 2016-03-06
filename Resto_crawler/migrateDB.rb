#Script to migrate the json data for reviews to rails sqlite database

#This script expects restaurants.json in the current directory
#Run the below command in your rails app home 
#bundle exec rails runner "eval(File.read 'migrateDB.rb')"

require 'json'

json = File.read('restaurants.json')
obj = JSON.parse(json)

number_of_restaurants = obj['restaurants'].count


for i in 0..number_of_restaurants - 1
	obj['restaurants'][i].each do |key, value|
	   res_id = key
	   name = value["name"]
	   photo_url = value["photo_url"]

       yelp_id = "yelp_" + res_id
	   yelp_rating = value['data']['yelp']['rating']
	   yelp_url = value['data']['yelp']['url']
	   yelp_ratings_count = value['data']['yelp']['count']
	   yelp_reviews = value['data']['yelp']['reviews']

       ta_id = "ta_" + res_id
       ta_rating = value['data']['tripadvisor']['rating']
	   ta_url = value['data']['tripadvisor']['url']
	   ta_ratings_count = value['data']['tripadvisor']['count']
	   ta_reviews = value['data']['tripadvisor']['reviews']

       fs_id = "fs_" + res_id
	   fs_rating = value['data']['foursquare']['rating']
	   fs_url = value['data']['foursquare']['url']
	   fs_ratings_count = value['data']['foursquare']['count']
	   fs_reviews = value['data']['foursquare']['reviews']

       #save in db
	   review = Review.new :res_id=>res_id, :yelp_id=>yelp_id, :ta_id=>ta_id, 
	              :fs_id=>fs_id, :name=>name, :photo_url=>photo_url
	   review.save

	   yelp_review = YelpReview.new :yelp_id=>yelp_id, :rating=>yelp_rating, 
	              :scale=>5, :url=>yelp_url, :ratings_count=>yelp_ratings_count, :reviews=>yelp_reviews
	   yelp_review.save

	   tripadvisor_review = TripadvisorReview.new :ta_id=>ta_id, :rating=>ta_rating, 
	              :scale=>5, :url=>ta_url, :ratings_count=>ta_ratings_count, :reviews=>ta_reviews
	   tripadvisor_review.save

	   foursquare_review = FoursquareReview.new :fs_id=>fs_id, :rating=>fs_rating, 
	              :scale=>10, :url=>fs_url, :ratings_count=>fs_ratings_count, :reviews=>fs_reviews
	   foursquare_review.save
	end
end
