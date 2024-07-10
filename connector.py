import mysql.connector

def connect():
    db = mysql.connector.connect(host="losvernos.com", user="root", password="Ynov2024ShadowOfTheErdtree", database="platonicus")
    if db.is_connected():
        print("Connected to database")
    else:
        print("Failed to connect to database")

    return db

