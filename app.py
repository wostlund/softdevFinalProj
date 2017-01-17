#!/usr/bin/python

import random
import csv
import hashlib
import os
from flask import Flask, render_template, request, session, url_for
#from utils import etsy, amazon, auth
from utils import etsy, auth

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
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "Welcome, " + session["username"] + "!")
	return render_template('main.html', title = "Ctrl.Alt.Gift", message = "")

@app.route("/login", methods = ["POST", "GET"])
def login():
	form = request.form
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
			return render_template('main.html', title = "Ctrl.Alt.Gift", message = "Welcome, " + session["username"]);
		else:
			return render_template('login.html', title = "Login", message = "Invalid Username or Password!");
	return render_template('login.html', title = "Login", message = "");

@app.route("/search", methods = ["POST", "GET"])
def search():
	if ("username" in session):
 		return render_template('search.html', title = "Search", login = "login", message = "");
	else:
	 	return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/shop", methods = ["POST", "GET"])
def shop():
	form = request.form
	if ("username" in session):
		searchstring = form["search"]
		return render_template('shop.html', login = "login", title = "Search", etsylist = etsy.search(searchstring, 24, price), message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/creategroup", methods = ["POST", "GET"])
def creategroup():
	if ("username" in session):
		return render_template('creategroup.html', login = "login", title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
	if ("username" in session):
		return render_template('idashboard.html', login = "login", title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/blacklist", methods = ["POST", "GET"])
def blacklist():
	if ("username" in session):
		return render_template('editblack.html', login = "login", title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/group", methods = ["POST", "GET"]) #Needs UNIQUE URL
def group():
	if ("username" in session):
		return render_template('editblack.html', login = "login", title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

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
    makefile()
    app.run()
