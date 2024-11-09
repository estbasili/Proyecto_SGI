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

# Obtener un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = Proveedor.get_proveedor_by_id(id)
        if proveedor:
            return jsonify(proveedor), 200
        return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Crear un nuevo proveedor
@proveedor_bp.route('/proveedores', methods=['POST'])
def create_proveedor():
    try:
        data = request.get_json()
        if not Proveedor.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400
        proveedor = Proveedor.create_proveedor(data)
        return jsonify(proveedor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Actualizar un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        if not Proveedor.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400
        proveedor = Proveedor.update_proveedor(id, data)
        if proveedor:
            return jsonify(proveedor), 200
        return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        proveedor = Proveedor.delete_proveedor(id)
        if proveedor:
            return jsonify({"mensaje": "Proveedor eliminado"}), 200
        return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400