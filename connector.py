import mysql.connector

def connect():
    # db = mysql.connector.connect(host="losvernos.com", user="root", password="Ynov2024ShadowOfTheErdtree", database="platonicus")
    db = mysql.connector.connect(host="localhost", user="root", password="", database="platonicus")
    db.autocommit = True
    if db.is_connected():
        print("Connected to database")
    else:
        print("Failed to connect to database")

    return db

