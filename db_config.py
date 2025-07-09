import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP’s default MySQL password is empty unless you set one
        database="school_ai_complaints"
    )
    return connection
