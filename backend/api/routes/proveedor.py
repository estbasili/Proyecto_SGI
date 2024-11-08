from flask import Blueprint, request, jsonify
from models.proveedor import Proveedor
#from api import app

proveedor_bp = Blueprint('proveedor', __name__)

@proveedor_bp.route('/proveedores', methods=['GET'])
def get_all_proveedores():
    try:
        proveedores = Proveedor.get_all_proveedores()
        return jsonify(proveedores), 200
        #return jsonify({"mensaje": "Prueba exitosa"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
