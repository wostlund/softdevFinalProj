#!/usr/bin/python

import random
import csv
import hashlib
import os
from flask import Flask, render_template, request, session, url_for
from utils import etsy, amazon, auth


app = Flask(__name__)
app.secret_key = 'secrets'

@app.route("/", methods = ["POST", "GET"])
def root():
	db = auth.connect()
	form = request.form
	if ("logout" in form):
		user = session["username"]
		session.pop("username")
		auth.disconnect(db)
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "You have been logged out!")
	if ("username" in session):
		auth.disconnect(db)
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "Welcome, " + session["username"] + "!")
	auth.disconnect(db)
	return render_template('main.html', title = "Ctrl.Alt.Gift", message = "")

@app.route("/login", methods = ["POST", "GET"])
def login():
	db = auth.connect()
	form = request.form
	if ("login" in form):
		if (auth.login(form["username"], form["password"]) == 0):
			session["username"] = form["username"]
			auth.disconnect(db)
			return render_template('main.html', title = "Ctrl.Alt.Gift", message = "Welcome, " + session["username"]);
		else:
			auth.disconnect(db)
			return render_template('login.html', title = "Login", message = "Invalid Username or Password!");
	auth.disconnect(db)
	return render_template('login.html', title = "Login", message = "");

@app.route("/search", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('search.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/shop", methods = ["POST", "GET"])
def shop():
	form = request.form
	if ("username" in session):
		searchstring = form["search"]
		return render_template('shop.html', title = "Search", etsylist = etsy.search(searchstring, 25), message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/creategroup", methods = ["POST", "GET"])
def creategroup():
	if ("username" in session):
		return render_template('creategroup.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
	if ("username" in session):
		return render_template('idashboard.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/blacklist", methods = ["POST", "GET"])
def blacklist():
	if ("username" in session):
		return render_template('editblack.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");


if __name__ == "__main__":
    app.debug = True 
    app.run()