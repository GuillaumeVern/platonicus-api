from MySQLdb import _mysql

def connect():
    return _mysql.connect("localhost", "root", "", "platonicus")
