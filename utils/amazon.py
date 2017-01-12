#!/usr/bin/python
import json, urllib2, datetime
from amazonproduct import API

##############
### AMAZON ###
##############

api = API(locale='en')

def search(terms, number, price);
	print api.item_search('Blended', Keywords=terms);

key = open("keys.txt", "r").read().strip().split("\n")[0]
# baseurl = """http://webservices.amazon.com/onca/xml?Service=AWSECommerceService
# 			&Operation=ItemSearch
# 			&AWSAccessKeyId=""" + key + """
# 			&Operation=ItemSearch
# 			&IncludeReviewsSummary=True
# 			&MaximumPrice=""" + price + """
# 			&Keywords=""" + terms + """
# 			&ResponseGroup=ItemAttributes,Offers,Images,Reviews,Variations
# 			&Version=2013-08-01
# 			&SearchIndex=All
# 			&Sort=salesrank
# 			"""
			#&AssociateTag=mytag-20

#test

# def search(terms, number, price): #price as a number (ie $20.00 is 2000)
# 	baseurl = """http://webservices.amazon.com/onca/xml?Service=AWSECommerceService
# 			&Operation=ItemSearch
# 			&AWSAccessKeyId=""" + key + """
# 			&Operation=ItemSearch
# 			&IncludeReviewsSummary=True
# 			&MaximumPrice=""" + str(price) + """
# 			&Keywords=""" + terms + """
# 			&ResponseGroup=ItemAttributes,Offers,Images,Reviews,Variations
# 			&Version=2013-08-01
# 			&SearchIndex=All
# 			&Sort=salesrank
# 			"""
# 	print baseurl
# 	# curr = urllib2.urlopen(url)
# 	# req = curr.read()
# 	# data = json.loads(req)

# search("donkey", 10, 2000)
