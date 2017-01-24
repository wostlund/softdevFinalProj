#!/usr/bin/python

import random
import csv
import hashlib
import os
from flask import Flask, render_template, request, session, url_for, redirect
#from utils import etsy, amazon, auth
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
	print form
	if ("register" in form):
		if (auth.register(form["name"], form["username"], form["password"]) == 0):
			return render_template('login.html', title = "Login", message = "Your account was successfully registered!");
		else:
			return render_template('login.html', title = "Login", message = "Your registration is invalid!");
	if ("login" in form):
		print "login initiated"
		print form["username"]
		print form["password"]
		print auth.login(form["username"], form["password"])
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
		return render_template('shop.html', login = "login", title = "Search", etsylist = elist , message = elist)
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/creategroup", methods = ["POST", "GET"])
def creategroup():
	form = request.form
	if ("username" in session):
		if ("creategroup" in form):
			print "Creating Group";
			gid = data.add_group(form["groupname"], form["budget"], form["exchange-date"], form["invites"])
			print gid
			return redirect(url_for('group', idnum = gid))
		return render_template('creategroup.html', login = "login", title = "Search", message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
	form = request.form
	if ("username" in session):
		# if ("update-blacklist-button" in form):
		# 	newblack = form["edited-blacklist"]
		# 	#Do the function to change text blacklist to list
		print session["username"]
		gdict = data.get_groups_dict(session["username"]);
		print gdict

		
		#return render_template('idashboard.html', mygroupslist = gdict, blacklist = data.get_blacklist(session["username"]), shoppinglist = [], login = "login", title = "Search", message = "")
		return render_template('idashboard.html', mygroupslist = gdict, blacklist = [], shoppinglist = [], login = "login", title = "Search", message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/blacklist", methods = ["POST", "GET"])
def blacklist():
	if ("username" in session):
		return render_template('editblack.html', myblacklist = "", login = "login", title = "Search", message = "")
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!")

@app.route("/group/<idnum>", methods = ["POST", "GET"])
def group(idnum):
	if ("username" in session):
		usergroups = data.get_groups_list(session["username"]);
		if (idnum in usergroups):
			ginfo = data.get_group_data(idnum)
			return render_template('group.html', pairuser = "", wishlist = [], members = "", groupinfo = ginfo, login = "login", title = "", message = ginfo)
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
