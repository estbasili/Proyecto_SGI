# backend/app.py
from flask import Flask
from db.db import init_db, get_db_connection
from models.producto import Producto
from routes.producto import producto_bp
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa la base de datos
init_db(app)

# Registra el blueprint de rutas de producto
app.register_blueprint(producto_bp)

@app.route('/prueba', methods=['GET'])
def prueba():
    return "prueba"

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        # Aquí pasamos 'app' a la función get_db_connection()
        connection = get_db_connection(app)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM producto")  # Cambia "productos" por tu tabla
        productos = cursor.fetchall()
        cursor.close()
        connection.close()
        return {'productos': productos}
    except DBError as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
