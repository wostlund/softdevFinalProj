#!/usr/bin/python
import json, urllib2, datetime
from amazonproduct import API

##############
### AMAZON ###
##############

#Dependencies: pip install python-amazon-product-api
#Dependencies: pip install lxml

api = API(locale='us')

def search(terms, number, price):
	print api.item_search('Blended', Keywords=terms);


search("donkey", 10, 2000)


