from flask import Blueprint, request, jsonify
from models.orden import Orden

orden_bp = Blueprint('orden', __name__)

# Obtener todas las órdenes
@orden_bp.route('/ordenes', methods=['GET'])
def get_all_ordenes():
    try:
        ordenes = Orden.get_all_ordenes()
        return jsonify(ordenes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

# Obtener una orden por ID
@orden_bp.route('/ordenes/<int:id>', methods=['GET'])
def get_orden_by_id(id):
    try:
        orden = Orden.get_orden_by_id(id)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Crear una nueva orden
@orden_bp.route('/ordenes', methods=['POST'])
def create_orden():
    try:
        data = request.get_json()
        if not Orden.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400
        orden = Orden.create_orden(data)
        return jsonify(orden), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

# Actualizar una orden existente
@orden_bp.route('/ordenes/<int:id>', methods=['PUT'])
def update_orden_by_id(id):
    try:
        data = request.get_json()
        if not Orden.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400
        orden = Orden.update_orden_by_id(id, data)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Eliminar una orden
@orden_bp.route('/ordenes/<int:id>', methods=['DELETE'])
def delete_orden_by_id(id):
    try:
        result = Orden.delete_orden_by_id(id)
        if result:
            return jsonify({"mensaje": "Orden eliminada exitosamente"}), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400