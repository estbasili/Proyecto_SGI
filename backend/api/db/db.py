import mysql.connector
import os

def get_db_connection():
    """
    Establece y devuelve la conexión a la base de datos.
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection

class DBError(Exception):
    """
    Clase de excepción personalizada para errores de la base de datos.
    """
    pass
