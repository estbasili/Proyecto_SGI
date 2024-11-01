import mysql.connector

def init_db(app):
    # Configura la aplicación con los datos de conexión directamente
    app.config['DB_HOST'] = 'localhost'  # Cambia esto a tu host
    app.config['DB_PORT'] = '3306'  # Cambia esto a tu puerto si es diferente
    app.config['DB_USER'] = 'root'  # Cambia esto a tu usuario
    app.config['DB_PASSWORD'] = ''  # Cambia esto a tu contraseña
    app.config['DB_NAME'] = 'gestion_inventario'  # Cambia esto a tu nombre de base de datos

def get_db_connection(app):
    # Crea la conexión usando los datos de configuración de la app
    connection = mysql.connector.connect(
        host=app.config['DB_HOST'],       # Usar configuración de host
        port=app.config['DB_PORT'],       # Usar configuración de puerto
        user=app.config['DB_USER'],       # Usar configuración de usuario
        password=app.config['DB_PASSWORD'],# Usar configuración de contraseña
        database=app.config['DB_NAME']    # Usar configuración de base de datos
    )
    return connection

class DBError(Exception):
    pass
