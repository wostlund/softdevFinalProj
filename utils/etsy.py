#!/usr/bin/python
import json, urllib2, datetime

############
### ETSY ###
############

key = open("keys.txt", "r").read().strip().split("\n")[1]
baseurl = "https://openapi.etsy.com/v2"


