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
def add_user(username, password, name):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower()
        req = "INSERT INTO userdata VALUES \
               ('%s','%s','%s')"%(username, password, name)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

def add_group(username, groupname, budget, date, users):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower().strip()
        gid = (int)(largest_groupid()) + 1

        # Creating Group
        req = "INSERT INTO groupdata VALUES \
               (%s, '%s', %s, '%s', '%s')"%(gid, groupname, 0, budget, date)
        c.execute(req)
        disconnect(db)
        
        # Adding Members
        users = parse_textarea(users)
        add_user_to_group(username, gid)
        print users # Debugging
        for entry in users:
            entry = entry.lower().strip()
            print add_user_to_group(entry, gid) # Debugging

        # Shuffling Members
        if (shuffle_group(gid) == False):
            remove_group(gid)
            return -1 # Impossible Shuffle
        
        print get_group_data(gid) # Debugging
        return gid
    except:
        return -2

# Untested
def add_blacklist(username, ignoreuser):
    try:
        username = username.lower()
        ignoreuser = ignoreuser.lower()
        if (username == ignoreuser):
            return False 
        if (user_exists(ignoreuser) == 1 
            and check_duplicate(username, ignoreuser) == 0):
            db = connect()
            c = db.cursor()
            ignorename = get_name(ignoreuser)
            req = "INSERT INTO blacklists VALUES \
                   ('%s', '%s', '%s')"%(username, ignoreuser, ignorename)
            c.execute(req)
            disconnect(db)
            return True
        return False
    except:
        return False
    
# Untested
def add_list(listtype, username, itemname, link):
    try:
        db.connect()
        c = db.cursor()
        username = username.lower()
        req = "INSERT INTO %s VALUES \
               ('%s', '%s', '%s')"%(listtype, username, itemname, link)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False
    
# Untested - Obsoleted
def add_wishlist(username, itemname, link=None):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower()
        if link is None:
            link = "N/A"
        req = "INSERT INTO wishlists VALUES \
               ('%s', '%s', '%s')"%(username, itemname, link)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False  

# Untested - Obsoleted
def add_shoppinglist(username, itemname, link):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower()
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
        # username = username.lower().strip() # Should be lowercase already.
        if (user_exists(username) == 0):
            return False
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

# Database - Data Removal
# ==========================================================================
def remove_blacklist(username, removeuser):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower()
        req = "DELETE FROM blacklists \
               WHERE username == '%s' AND ignoreuser == '%s'"%(username, removeuser)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

# Untested
def remove_list(listtype, username, itemname, link):
    try:
        db = connect()
        c = db.cursor()
        username = username.lower()
        req = "DELETE FROM %s \
               WHERE username == '%s' AND itemname == '%s' AND link == '%s'"%(listtype, username, itemname, link)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

def remove_group(gid):
    try:
        db = connect()
        c = db.cursor()
        req = "DELETE FROM groups \
               WHERE groupid == %s"%(gid)
        c.execute(req)
        req = "DELETE FROM groupdata \
               WHERE groupid == %s"%(gid)
        c.execute(req)
        disconnect(db)
        return True
    except:
        return False

# Database - Data Retrieval
# ==========================================================================
# Untested
def change_list(inputs): # inputs should be a dictionary
    try:
        listtype = inputs['submit'] # wishlists | shoppinglists
        username = inputs['username']
        itemname = inputs['name']
        link = inputs['link']
        task = inputs['task'] # add | remove
        if task == "add":
            return add_list(listtype, username, itemname, link)
        elif task == "remove":
            return remove_list(listtype, username, itemname, link)
        else:
            return False
    except:
        return False

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
        return {}

def get_groups_list(username):
    db = connect()
    c = db.cursor()
    username = username.lower()
    req = "SELECT groupid FROM groups WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = []
    for entry in data:
        ret += [entry[0]]
    disconnect(db)
    return ret
                    
def get_groups_dict(username):
    username = username.lower()

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
    return names

# Untested
def get_wishlist(username):
    db = connect()
    c = db.cursor()
    username = username.lower()
    req = "SELECT * FROM wishlists WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = []
    for entry in data:
        tmp = {}
        tmp['name'] = entry[1]
        tmp['link'] = entry[2]
        ret += [tmp]
    disconnect(db)
    return ret

# Untested
def get_shoppinglist(username):
    db = connect()
    c = db.cursor()
    req = "SELECT * FROM shoppinglists WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = []
    for entry in data:
        tmp = {}
        tmp['name'] = entry[1]
        tmp['link'] = entry[2]
        ret += [tmp]
    disconnect(db)
    return ret

def get_name(username):
    db = connect()
    c = db.cursor()
    username = username.lower()
    req = "SELECT name FROM userdata WHERE username == '%s'"%(username)
    data = c.execute(req)
    ret = "N/A"
    for entry in data:
        ret = entry[0]
    disconnect(db)
    return ret

def get_recipient(groupid, username):
    db = connect()
    c = db.cursor()
    username = username.lower()
    req = "SELECT recipient FROM groups WHERE groupid == %s AND username == '%s'"%(groupid, username)
    data = c.execute(req)
    ret = "N/A"
    for entry in data:
        ret = entry[0]
    disconnect(db)
    return ret

def get_blacklist(username): # Username Of Person Logged In
    db = connect()
    c = db.cursor()
    username = username.lower()
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
        if mem < 2:
            return False # Not Enough Members, Shuffle Fails

        req = "SELECT * FROM groups WHERE groupid = %s"%(groupid)
        c.execute(req)

        # Building Shuffle Array
        tmp = []
        for i in c:
            tmp += [[i[1], i[2]]]
        for i in range(7 * mem):
            swap(tmp, random.randint(0, mem-1), random.randint(0, mem-1))

        # Blacklist Shuffle
        blacklists = []
        for i in range(len(tmp)):
            ignore = get_blacklist(tmp[i][0])
            ignore_add = []
            for j in ignore:
                ignore_add += [j[0]]
            blacklists += [ ignore_add ] # Indexed Correctly
        ''' # Debugging
        for i in blacklists:
            print i
        print "==================="
        '''
        retval = False
        people = [i[0] for i in tmp]
        path = [] # Solution Set
        seed = people[0]        
        tested = [seed] # Nodes In Graph
        tests = [] # Connections To New Nodes
        test_count = 0 # Number of Tests

        # Seeding Tests
        test_count += add_tests(tests, seed, people, tested, blacklists[0])
        #while (index < tests): # Calling len is inefficient
        ''' # Debugging
        print people
        print tests
        print tested
        print test_count
        print "==================="
        '''
        while (test_count > 0):
            next_test = tests.pop()
            test_count -= 1
            next_node = next_test[1]
            while (tested[-1] != next_test[0]):
                tested.pop()
            tested += [next_node]
            tests_added = add_tests(tests, next_node, people, tested, 
                                    blacklists[people.index(next_node)])
            test_count += tests_added

            if tests_added == 0: # No More Paths Left
                if (len(tested) == len(people) and
                    people[0] not in blacklists[people.index(tested[-1])]):
                    '''# Debugging
                    print people # Original Ordering
                    print tested # Final Ordering
                    return "FOUND"
                    '''
                    # Updating Database - Successful
                    for i in range(len(people)):
                        req = "UPDATE groups \
                               SET recipient = '%s' \
                               WHERE username == '%s'"%(tested[i], tested[i-1])
                        c.execute(req)
                    retval = True
                    break;
                else:
                    tested.pop()
            ''' # Debugging    
            print "\n", tests
            print tests_added, " | ", tested
            '''

        '''
        # Non Blacklist Shuffle
        # The Shuffle
        for i in range(mem):
            tmp[i][1] = tmp[i-1][0]
        #for i in tmp:
        #   print i # Debugging


        # Updating Database
        for i in tmp:
            req = "UPDATE groups \
                   SET recipient = '%s' \
                   WHERE username == '%s'"%(i[1], i[0])
            c.execute(req)
        '''
        disconnect(db)
        return retval
    except:
        return False
    
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

def check_duplicate(username, ignoreuser):
    db = connect()
    c = db.cursor()
    username = username.lower()
    ignoreuser = ignoreuser.lower()
    req = "SELECT EXISTS \
           ( SELECT 1 FROM blacklists \
           WHERE username == '%s' AND ignoreuser == '%s' )"%(username, ignoreuser)
    data = c.execute(req)
    ret = -1
    for i in data:
        ret = i[0]
    disconnect(db)
    return ret

def add_tests(tests, user, users, tested, blacklist):
    # tests - array buffer
    # user - user to expand cases
    # users - userlist
    # blacklist - blacklist of user
    add = []
    for person in users:
        if person not in blacklist and person not in tested and person != user:
                add += [[user, person]][::-1]
    tests += add
    return len(add)

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
