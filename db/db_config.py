import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestion_inventario"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    return None
