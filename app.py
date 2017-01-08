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
		return render_template('main.html', title = "Login", message = "You have been logged out!", flag = "logout")
	if ("username" in session):
		return render_template('main.html', title = "Landing", message = "Welcome, " + session["username"] + "!", flag = "login")
	return render_template('main.html', title = "Login", message = "Enter your username and password:", flag = "logout")
	return "Main Page";

@app.route("/login", methods = ["POST", "GET"])
def login():
	form = request.form
	if ("login" in form):
		session["username"] = username;
		return "Main Page";
	return "Login Page";

@app.route("/search", methods = ["POST", "GET"])
def search():
	return "Search Page";

@app.route("/shop", methods = ["POST", "GET"])
def search():
	return "Shop Page";

@app.route("/creategroup", methods = ["POST", "GET"])
def search():
	return "Create Group Page";

@app.route("/dashboard", methods = ["POST", "GET"])
def search():
	return "Dashboard Page";

@app.route("/blacklist", methods = ["POST", "GET"])
def search():
	return "Blacklist Page";


if __name__ == "__main__":
    app.debug = True 
    app.run()