# ========================================
# Database Module
# ========================================

import sqlite3, random

def connect():
    name = "./utils/data.db" # Change
    db = sqlite3.connect(name)
    return db

def disconnect(db):
    db.commit()
    db.close()

# Table Initialization Functions
# ==========================================================================
def init():
    db = connect()
    c = db.cursor()
    # Creating Tables
    cmdlist = ["CREATE TABLE IF NOT EXISTS groups \
               (groupid INTEGER, username TEXT, recipient TEXT)",
               "CREATE TABLE IF NOT EXISTS groupdata \
               (groupid INTEGER, groupname TEXT, members INTEGER)",
               "CREATE TABLE IF NOT EXISTS userdata \
               (username TEXT, password TEXT, name TEXT)",
               "CREATE TABLE IF NOT EXISTS wishlists \
               (username TEXT, itemname TEXT, link TEXT)",
               "CREATE TABLE IF NOT EXISTS blacklists \
               (username TEXT, ignoreuser TEXT, ignorename TEXT)",
               "CREATE TABLE IF NOT EXISTS shoppinglists \
               (username TEXT, itemname TEXT, link TEXT)"]
    for cmd in cmdlist:
        c.execute(cmd)
    disconnect(db)

def reset():
    db = connect()
    c = db.cursor()
    # Delete Entries
    tablelist = ["groups", "groupdata", "userdata", "wishlists", "blacklists", "shoppinglists"]
    for table in tablelist:
        cmd = "DELETE FROM %s"%(table)
        c.execute(cmd)
    disconnect(db)
    
# Database Editing Functions
# ==========================================================================
def add_user(username, password, name, email):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO userdata VALUES \
               ('%s','%s','%s')"%(username, password, name)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

def add_group(groupname):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO groupdata VALUES \
               (%s, '%s', %s)"%(int(largest_groupid()) + 1, groupname, 0)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

# Untested
def add_blacklist(username, ignoreuser, ignorename):
    return 0
    
# Untested
def add_wishlist(username, itemname, link=None):
    try:
        db = connect()
        c = db.cursor()
        if link is None:
            link = "N/A"
        req = "INSERT INTO wishlists VALUES \
               (%s, '%s', %s)"%(username, itemname, link)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False  

# Untested
def add_shoppinglist(username, itemname, link):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO shoppinglists VALUES \
               (%s, '%s', %s)"%(username, itemname, link)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False  

    
def add_user_to_group(username, groupid):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO groups VALUES \
               (%s, '%s', '%s')"%(groupid, username, username) # Unshuffled
        c.execute(req)
        req = "UPDATE groupdata \
               SET members = members + 1 \
               WHERE groupid = %s"%(groupid)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

def shuffle_group(groupid):
    try:
        db = connect()
        c = db.cursor()

        # Preliminary Checks
        req = "SELECT members FROM groupdata WHERE groupid = %s"%(groupid)
        c.execute(req)
        mem = 0
        for i in c:
            mem = i[0]
        if mem == 0:
            return False # No Members, Shuffle Fails

        req = "SELECT * FROM groups WHERE groupid = %s"%(groupid)
        c.execute(req)

        # Building Shuffle Array
        tmp = []
        for i in c:
            tmp += [[i[1], i[2]]]
        for i in range(7 * mem):
            swap(tmp, random.randint(0, mem-1), random.randint(0, mem-1))
        for i in range(mem):
            tmp[i][1] = tmp[i-1][0]
        #for i in tmp:
        #   print i # Debugging

        # Updating Database
        for i in tmp:
            req = "UPDATE groups \
                   SET recipient = '%s' \
                   WHERE username = '%s'"%(i[1], i[0])
            c.execute(req)

        disconnect(db)
        return True
    except:
        return False
    
# Helper Functions
# ==========================================================================
def largest_groupid():
    db = connect()
    c = db.cursor()
    req = "SELECT groupid FROM groupdata"
    data = c.execute(req)
    maxid = -1
    for entry in data:
        if entry[0] > maxid:
            maxid = entry[0]
    disconnect(db)
    return maxid

def swap(array, i1, i2):
    tmp = array[i1]
    array[i1] = array[i2]
    array[i2] = tmp

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    try:
        reset()
    except:
        init()
        reset()    
