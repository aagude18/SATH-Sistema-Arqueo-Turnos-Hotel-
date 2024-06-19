import mysql.connector

def mydb_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='base_hotel'
    )
    return mydb