from api import app
from api.db.db import DBError
from flask import request, jsonify
from api.models.estado import Estado
@app.route('/estados', methods=['GET'])
def get_estados():
    try:
        estados = Estado.get_all_estados()
        return jsonify(estados), 200 
    except DBError as e:
        return jsonify({"message": str(e)}), 203
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500