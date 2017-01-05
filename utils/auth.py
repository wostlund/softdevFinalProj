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

def login(username, password):
    db = connect();
    c = db.cursor;
