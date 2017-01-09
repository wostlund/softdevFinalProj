#!/usr/bin/python

import random
import csv
import hashlib
import os
from flask import Flask, render_template, request, session, url_for


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
	if ("login" in form):
		session["username"] = username;
		return render_template('main.html', title = "Ctrl.Alt.Gift", message = "");
	return render_template('login.html', title = "Login", message = "");

@app.route("/search", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('search.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/shop", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('shop.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/creategroup", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('creategroup.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/dashboard", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('idashboard.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");

@app.route("/blacklist", methods = ["POST", "GET"])
def search():
	if ("username" in session):
		return render_template('editblack.html', title = "Search", message = "");
	else:
		return render_template('login.html', title = "Login", message = "You must log in to continue!");


if __name__ == "__main__":
    app.debug = True 
    app.run()