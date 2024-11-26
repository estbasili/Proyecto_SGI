import logging
from flask import Flask, jsonify
from api.db.db import  get_db_connection, DBError
from dotenv import load_dotenv
from flask_cors import CORS

# Configura la app para capturar logs detallados
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

@app.route('/')
def test():
    return jsonify({"message": "test ok"})


import api.routes.usuario
import api.routes.producto
import api.routes.proveedor
import api.routes.categoria
import api.routes.orden
import api.routes.estado

