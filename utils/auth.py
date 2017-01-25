# ========================================
# Authentication Module
# ========================================

import sqlite3, hashlib

def connect():
    name = "./utils/data.db" # Change
    db = sqlite3.connect(name)
    return db

def disconnect(db):
    db.commit()
    db.close()

# Authentication Functions
# ==========================================================================
def login(username, password):
    try:
        username = username.lower().strip()
        if check_safe(username) < 0:
            return -2 # Invalid Username
        db = connect()
        c = db.cursor()
        req = "SELECT * FROM userdata WHERE username == '%s'"%(username)
        data = c.execute(req)
        fields = [i for i in data]
        if len(fields): # User is registered.
            data = fields[0][1]
            if data == browns(password):
                return 0 # Correct Password
            return -1 # Incorrect Password
        return -2 # Invalid Username
    except:
        return -3 # Fatal Error

def register(name, username, password):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower().strip()
        if check_safe(username) < 0 or user_exists(username):
            return -1 # Invalid Username
        req = "INSERT INTO userdata VALUES \
               ('%s','%s','%s')"%(username, browns(password), format_caps(name))
        c.execute(req)
        disconnect(db)
        return 0 # Success
    except:
        return -2 # Failure

def change_password(username, oldpass, newpass):
    try:
        if login(username, oldpass) == 0:
            db = connect()
            c = db.cursor()
            req = "UPDATE userdata \
                   SET password = '%s' \
                   WHERE username = '%s'"%(browns(newpass), username)
            c.execute(req)
            disconnect(db)
            return 0
        return -1 # Failure
    except:
        return -2 # Failure
        
# Helper Functions
# ==========================================================================
def user_exists(username):
    db = connect()
    c = db.cursor()
    username = username.lower()
    req = "SELECT EXISTS \
           ( SELECT 1 FROM userdata WHERE username == '%s' )"%(username)
    data = c.execute(req)
    ret = -1
    for i in data:
        ret = i[0]
    disconnect(db)
    return ret

def check_safe(username):
    if (username == "drop tables"):
        return -2 # You think you're clever, don't you.
    good = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
    for char in username:
        if char not in good:
            return -1 # Invalid Character
    return 0 # Good

def browns(password):
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
