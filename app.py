#!/usr/bin/python

import random
import csv
import hashlib
import os
import json
from flask import Flask, render_template, request, session, url_for, redirect
from utils import etsy, auth, data

app = Flask(__name__)
app.secret_key = 'secrets'

@app.route("/", methods = ["POST", "GET"])
def root():
	form = request.form
	if ("logout" in form):
		user = session["username"]
		session.pop("username")
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "You have been logged out!")
	if ("username" in session):
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "")
	return render_template('main.html', title = "Ctrl.Alt.Gift", message = "")

@app.route("/logout", methods = ["POST", "GET"])
def logout():
	user = session["username"]
	session.pop("username")
	return render_template('main.html', title = "Ctrl.Alt.Gift", message = "You have been logged out!")


@app.route("/login", methods = ["POST", "GET"])
def login():
	form = request.form
	if ("register" in form):
		if (auth.register(form["name"], form["username"], form["password"]) == 0):
			return render_template('login.html', title = "Login", message = "Your account was successfully registered!");
		else:
			return render_template('login.html', title = "Login", message = "Your registration is invalid!");
	if ("login" in form):
		if (auth.login(form["username"], form["password"]) == 0):
			session["username"] = form["username"]
			return redirect(url_for('dashboard'))
		else:
			return render_template('login.html', title = "Login", message = "Invalid Username or Password!")
	return render_template('login.html', title = "Login", message = "")

@app.route("/search", methods = ["POST", "GET"])
def search():
	if ("username" in session):
 		return render_template('search.html', title = "Search", login = "login", message = "")
	else:
	 	return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/shop", methods = ["POST", "GET"])
def shop():
	form = request.form
	if ("username" in session):
		searchstring = form["searchstring"]
		elist = etsy.search(searchstring, 24)
		return render_template('shop.html', login = "login", title = "Search", etsylist = elist , message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/creategroup", methods = ["POST", "GET"])
def creategroup():
	form = request.form
	if ("username" in session):
		if ("creategroup" in form):
			gid = data.add_group(session["username"], form["groupname"], form["budget"], form["exchange-date"], form["invites"])
			if (gid < 0):
				return redirect(url_for('dashboard', message="Group could not be created!"))
			return redirect(url_for('group', idnum = gid))
		return render_template('creategroup.html', login = "login", title = "Search", message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
	form = request.form
	if ("username" in session):
		if ("remWishList" in form):
			data.remove_list("wishlists", session["username"], form["name"], form["link"])
		if ("remShoppingList" in form):
			data.remove_list("shoppinglists", session["username"], form["name"], form["link"])
		gdict = data.get_groups_dict(session["username"])
		blist = data.get_blacklist(session["username"])
		wlist = data.get_wishlist(session["username"])
		slist = data.get_shoppinglist(session["username"])
		return render_template('idashboard.html', mygroupslist = gdict, blacklist = blist, wishlist = wlist, shoppinglist = slist, title = "Dashboard", message = "")
		
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/blacklist", methods = ["POST", "GET"])
def blacklist():
	form = request.form
	if ("username" in session):
		blist = data.get_blacklist(session["username"])
		if ("remove-blacklist-button" in form):
			data.remove_blacklist(session["username"], form["username"])
			blist = data.get_blacklist(session["username"])
			return render_template('editblack.html', myblacklist = blist, login = "login", title = "Blacklist", message = "")
		if ("add-blacklist-button" in form):
			data.add_blacklist(session["username"], form["username"])
			blist = data.get_blacklist(session["username"])
			return render_template('editblack.html', myblacklist = blist, login = "login", title = "Blacklist", message = "")
		else:
			return render_template('editblack.html', myblacklist = blist, login = "login", title = "Blacklist", message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")


@app.route("/addtowish", methods = ["POST", "GET"])
def addtowish():
	if ("username" in session):
		blist = data.get_wishlist(session["username"])
                task = request.args.get("task")
                name = request.args.get("name")
                link = request.args.get("link")
                print(task)
                if (task == "remove"):
                        print("2134")
		        data.remove_list("wishlists", session["username"], name, link)
		        blist = data.get_wishlist(session["username"])
                        #return render_template('shop.html', login = "login", title = "Search", etsylist = blist , message = "Successfully Removed Item from Wishlist")
                        return json.dumps({})
		else:
			data.add_wishlist(session["username"], name, link)
			blist = data.get_wishlist(session["username"])
			#return render_template('shop.html', login = "login", title = "Search", etsylist = blist , message = "Successfully Added Item to Wishlist")
                        return json.dumps({})
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/addtoshop", methods = ["POST", "GET"])
def addtoshop():
	if ("username" in session):
		blist = data.get_wishlist(session["username"])
                task = request.args.get("task")
                name = request.args.get("name")
                link = request.args.get("link")
                print(task)
                if (task == "remove"):
                        #print("2134")
		        data.remove_list("shoppinglists", session["username"], name, link)
		        blist = data.get_shoppinglist(session["username"])
                        #return render_template('shop.html', login = "login", title = "Search", etsylist = blist , message = "Successfully Removed Item from Shopping list")
                        return json.dumps({})
		else:
			data.add_shoppinglist(session["username"], name, link)
			blist = data.get_shoppinglist(session["username"])
			#return render_template('shop.html', login = "login", title = "Search", etsylist = blist , message = "Successfully Added Item to Shopping list")
                        return json.dumps({})
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")    
        
@app.route("/group/<idnum>", methods = ["POST", "GET"])
def group(idnum):
	if ("username" in session):
		usergroups = data.get_groups_list(session["username"]);
		if int(idnum) in usergroups:
			recipient = data.get_recipient(idnum, session["username"])
			ginfo = data.get_group_data(idnum)
			wlist = data.get_wishlist(recipient)
			return render_template('group.html', pairuser = recipient, wishlist = wlist, memberlist = ginfo["membernames"], groupinfo = ginfo, login = "login", title = "", message = ginfo)
		else:
			return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")
	

def makefile():
	key = open("keys.txt", "r").read().strip().split("\n")[0]
	secret = open("keys.txt", "r").read().strip().split("\n")[2]
	tag = open("keys.txt", "r").read().strip().split("\n")[3]
	filetext = """[Credentials]\naccess_key = """ + key + """\nsecret_key = """ + secret + """\nassociate_tag = """ + tag
	home = os.getenv("HOME")
	f = open(home + "/.amazon-product-api", "w+")
	f.write(filetext)
	f.close()
	print " * Key File Generated!"

if __name__ == "__main__":
        app.debug = True 
        #makefile()
        app.run()
