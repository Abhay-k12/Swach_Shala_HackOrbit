import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP default password is empty unless changed
        database="swachh_shala"
    )
    return connection
