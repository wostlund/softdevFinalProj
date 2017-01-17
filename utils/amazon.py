#!/usr/bin/python
import json, urllib2, datetime, lxml
from amazonproduct import API
from lxml import objectify

##############
### AMAZON ###
##############

#Dependencies: pip install python-amazon-product-api
#Dependencies: pip install lxml

api = API(locale='us')

def search(terms, number, price):
	results = api.item_search('Blended', Keywords=terms)
	numresults = results.results
	numpages = results.pages
	for item in results.Items.Item:
		print item.ASIM
	print results
	print numresults
	print numpages


search("donkey", 10, 2000)


