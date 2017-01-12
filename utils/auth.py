# ========================================
# Authentication Module
# ========================================

import sqlite3, hashlib

def connect():
    name = "./data.db"
    db = sqlite3.connect(name)
    return db

def disconnect(db):
    db.commit()
    db.close()

# Authentication Functions
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

def register(name, username, password):
    try:
        db = connect()
        c = db.cursor
        req = "INSERT INTO userdata VALUES \
               ('%s','%s','%s','%s')"%(username, hash(password), format_caps(name))
        c.execute(req)
        disconnect(db)
        return 0 # Good
    except:
        return -1 # Failure


# Helper Functions
# ==========================================================================
def check_safe(username):
    if (username == "drop tables"):
        return -2 # You think you're clever, don't you.
    good = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
    for char in username:
        if char not in good:
            return -1 # Invalid Character
    return 0 # Good

def hash(password):
    password = password + "this-is-some-nice-salt-and-pepper"
    password = hashlib.sha384(password).hexdigest()
    return password

def format_caps(name):
    ret = ""
    switch = True
    for c in name:
        if switch:
            switch = False
            ret += c.upper()
        else:
            if c == " ":
                switch = True
            ret += c
    return ret
