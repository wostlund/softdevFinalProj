# ========================================
# Authentication Module
# ========================================

import sqlite3, hashlib

def connect():
    name = "./data/<NAME TO ADD HERE>.db"
    db = sqlite3.connect(name)
    return db
def disconnect(db):
    db.commit()
    db.close()

# Authorization Functions
# ==========================================================================
def login(username, password):
    username = username.lower()
    if check_safe(username) < 0:
        return -2 # Invalid Username
    db = connect()
    c = db.cursor
    req = "SELECT username FROM userdata WHERE username == '%s'"%(username)
    data = c.execute(req)
    if data: # User is registered.
        if data['password'] == hash(password):
            return 0 # Correct Password
        return -1 # Incorrect Password
    return -2 # Invalid Username

def check_safe(username):
    if (username == "drop tables"):
        return -2 # You think you're clever, don't you.
    good = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
    for char in username:
        if char not in good:
            return -1 # Invalid Character
    return 0 # Good

def hash(password): # To Implement
    password = password + "this-is-some-nice-salt-and-pepper"
    password = hashlib.sha384(password).hexdigest()
    return password
