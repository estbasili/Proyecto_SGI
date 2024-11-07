import logging
from flask import Flask, jsonify
from db.db import init_db, get_db_connection, DBError
from routes.proveedor import proveedor_bp  
from dotenv import load_dotenv
from flask_cors import CORS

# Configura la app para capturar logs detallados
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa la base de datos (configuración)
try:
    init_db(app)
except Exception as e:
    app.logger.error(f"Error al inicializar la base de datos: {e}")

# Registra los blueprints de rutas
app.register_blueprint(proveedor_bp)

@app.route('/')
def test():
    return jsonify({"message": "test ok"})


if __name__ == '__main__':
    try:
        app.run(debug=True, port=5001)
    except Exception as e:
        app.logger.error(f"Error al iniciar el servidor: {e}")
