import mysql.connector

def connect():
    db = mysql.connector.connect(host="localhost", user="root", password="", database="platonicus")
    if db.is_connected():
        print("Connected to database")
    else:
        print("Failed to connect to database")

    return db

