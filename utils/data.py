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
               (groupid INTEGER, groupname TEXT, members INTEGER, budget TEXT, date TEXT)",
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
    
# Database - Data Addition
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

def add_group(username, groupname, budget, date, users):
    #try:
        db = connect()
        c = db.cursor()
        gid = (int)(largest_groupid()) + 1

        # Creating Group
        req = "INSERT INTO groupdata VALUES \
               (%s, '%s', %s, '%s', '%s')"%(gid, groupname, 0, budget, date)
        c.execute(req)
        disconnect(db)
        
        # Adding Members
        users = parse_textarea(users)
        add_user_to_group(username, gid)
        print users
        for entry in users:
            add_user_to_group(entry, gid)

        # Shuffling Members
        shuffle_group(gid)
        
        print get_group_data(gid)
        return gid
    #except:
    #    return -1

# Untested
def add_blacklist(username, ignoreuser):
    try:
        db = connect()
        c = db.cursor()
        ignorename = get_name(username)
        req = "INSERT INTO blacklists VALUES \
              ('%s', '%s', '%s')"%(username, ignoreuser, ignorename)
        c.execute(req)
        disconnect(db)
    except:
        return False
    
# Untested
def add_wishlist(username, itemname, link=None):
    try:
        db = connect()
        c = db.cursor()
        if link is None:
            link = "N/A"
        req = "INSERT INTO wishlists VALUES \
               ('%s', '%s', '%s')"%(username, itemname, link)
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
               ('%s', '%s', '%s')"%(username, itemname, link)
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
        shuffle_group(groupid) # Shuffled
        req = "UPDATE groupdata \
               SET members = members + 1 \
               WHERE groupid = %s"%(groupid)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

# Database - Data Retrieval
# ==========================================================================
def get_group_data(groupid):
    try:
        db = connect()
        c = db.cursor()
        req = "SELECT * FROM groupdata WHERE groupid = %s"%(groupid)
        data = c.execute(req)
        ret = {} # Return
        for entry in data:
            ret['groupid'] = entry[0]
            ret['groupname'] = entry[1]
            ret['members'] = entry[2]
            ret['budget'] = entry[3]
            ret['date'] = entry[4]
        disconnect(db)
        ret['membernames'] = get_group_users(groupid)
        return ret
    except:
        return False

def get_groups_list(username):
    db = connect()
    c = db.cursor()
    req = "SELECT groupid FROM groups WHERE username == '%s'"%(username)
    data = c.execute(req)

    ret = []
    for entry in data:
        ret += [entry[0]]
    disconnect(db)

    return ret
                    
def get_groups_dict(username):

    # IDs
    ids = get_groups_list(username)

    # Parsing Names
    names = []

    db = connect()
    c = db.cursor()
    for i in ids:
        req = "SELECT groupname FROM groupdata WHERE groupid == %s"%(i)
        data = c.execute(req)
        for entry in data:
            names += [entry[0]]
    disconnect(db)
    ret = []
    for i in range(len(ids)):
        tmp = {}
        tmp['groupid'] = ids[i]
        tmp['groupname'] = names[i]
        ret += [tmp]

    return ret

def get_group_users(groupid):
    db = connect()
    c = db.cursor()
    req = "SELECT username FROM groups WHERE groupid == %s"%(groupid)
    data = c.execute(req)
    names = []
    for entry in data:
        names += [entry[0]]
    disconnect(db)
    return ret

def get_name(username):
    db = connect()
    c = db.cursor()
    req = "SELECT name FROM userdata WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = "N/A"
    for entry in data:
        ret = entry[0]
    disconnect(db)
    return ret

def get_blacklist(username): # Username Of Person Logged In
    db = connect()
    c = db.cursor()
    req = "SELECT * FROM blacklists WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = []
    for entry in data:
        i = [entry[1], entry[2]]
        ret += [i]
    disconnect(db)
    return ret
    
# Database - Data Modification
# ==========================================================================
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

def parse_textarea(text, delimiter=None):
    if delimiter is None:
        return text.strip().split()
    return text.strip().split(delimiter)

def groups():
    db = connect()
    c = db.cursor()
    req = "SELECT * FROM groupdata"
    data = c.execute(req)
    ret = []
    for i in data:
        ret += [i]
    disconnect(db)
    return ret        


# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    try:
        reset()
    except:
        init()
        reset()    
