# api/__init__.py

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def test():
    return jsonify({"message": "test ok"})

# Importamos y registramos los blueprints
from api.routes.proveedor import proveedor_bp
app.register_blueprint(proveedor_bp)
