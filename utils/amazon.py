#!/usr/bin/python
import json, urllib2, datetime

##############
### AMAZON ###
##############

key = open("../keys.txt", "r").read().strip().split("\n")[0]
baseurl = """http://webservices.amazon.com/onca/xml?Service=AWSECommerceService&
        	Operation=%s&
        	AWSAccessKeyId=%s&
        	AssociateTag=%s&
        	SubscriptionId=%s&
        	AssociateTag=%s&
        	SearchIndex=%s&
        	Keywords=%s&
        	ResponseGroup=%s"""