# db_config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='ARYan02@',
        database='bus_ticket_system'
    )
