#!/usr/bin/python
import json, urllib2, datetime

############
### ETSY ###
############

key = open("keys.txt", "r").read().strip().split("\n")[1]
baseurl = "https://openapi.etsy.com/v2/"



def search(terms, number): 
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
		newdict["price"] = i["price"] + " " + i["currency_code"]
		newdict["url"] = i["url"];
		try:
			imgs = i["Images"][0]; #dictionary
			newdict["imgurl"] = imgs["url_fullxfull"]
		except:
			newdict["imgurl"] = "No Images"
		reslist.append(newdict)
	return reslist

#print search("donkey", 25)
