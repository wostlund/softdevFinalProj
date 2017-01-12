#!/usr/bin/python
import json, urllib2, datetime

############
### ETSY ###
############

key = open("keys.txt", "r").read().strip().split("\n")[1]
baseurl = "https://openapi.etsy.com/v2/"



def search(terms, number, price): #add price controls!!
	urladd = "listings/active?keywords=" + terms + "&limit=" + str(number) + "&includes=Images:1&api_key=" + key
	url = baseurl + urladd
	curr = urllib2.urlopen(url)
	req = curr.read()
	data = json.loads(req)
	resdict = data["results"]
	reslist = []
	for i in resdict:
		newdict = {}
		newdict["name"] = i["title"]
		newdict["description"] = i["description"]
		newdict["category"] = i["category_path"]
		newdict["price"] = i["price"]
		intprice = int(float(newdict["price"]))
		newdict["currency"] = i["currency_code"]
		newdict["url"] = i["url"];
		imgs = i["Images"][0]; #dictionary
		newdict["imgurl"] = imgs["url_fullxfull"]
		if (intprice <= price):
			reslist.append(newdict)
	return reslist

#print search("donkey", 25, 20)
