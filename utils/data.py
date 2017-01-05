# ========================================
# Database Module
# ========================================

import sqlite3
import csv

# Table Initialization Functions
# ==========================================================================
def connect():
    name = "./data/<TABLE NAME HERE>.db"
    db = sqlite3.connect(name)
    return db

def disconnect(db):
    db.commit()
    db.close()

def init():
    db = connect()
    c = db.cursor()
    # Creating Tables
    # TO EDIT
    cmd = "CREATE TABLE IF NOT EXISTS userdata (username TEXT, password TEXT)"
    c.execute(cmd)
    disconnect(db)

def reset():
    db = connect()
    c = db.cursor()
    # Delete Entries
    # TO EDIT
    cmd = "DELETE FROM userdata"
    disconnect(db)
    
# Data Editing Functions
# ==========================================================================
def add_user(username, password):
    try:
        db = connect()
        c = db.cursor()
        req = "INSERT INTO userdata VALUES (?,?)"
        c.execute(req, (username,password))
        disconnect(db)
        return True
    except:
        return False

# Initialization
# ==========================================================================
if (__name__ == "__main__"):
    init()
