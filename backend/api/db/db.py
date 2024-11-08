# db.py
import mysql.connector
from mysql.connector import Error

# Mantén init_db como está
def init_db(app):
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_PORT'] = '3306'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = ''
    app.config['DB_NAME'] = 'gestion_inventario'

# Cambiar la firma de la función para no requerir el argumento 'app'
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Puedes usar estos valores directamente
            port='3306',       # Usar el puerto configurado
            user='root',       # Usuario de la base de datos
            password='',       # Contraseña de la base de datos
            database='gestion_inventario'  # Nombre de la base de datos
        )
        return connection
    except Error as e:
        raise DBError(f"Database connection error: {e}")

class DBError(Exception):
    pass
