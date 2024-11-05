# api/routes/proveedores.py

from flask import Blueprint, request, jsonify
from api.models.proveedor import Proveedor, DBError

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor_by_id(id):
    """Obtiene un proveedor por su ID."""
    try:
        proveedor = Proveedor.get_proveedor_by_id(id)
        return jsonify(proveedor), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404

@proveedor_bp.route('/proveedores', methods=['GET'])
def get_all_proveedores():
    """Obtiene todos los proveedores."""
    proveedores = Proveedor.get_all_proveedores()
    return jsonify(proveedores), 200

@proveedor_bp.route('/proveedores', methods=['POST'])
def add_proveedor():
    """Crea un nuevo proveedor."""
    data = request.json
    if not Proveedor.validate(data):
        return jsonify({"message": "Datos inválidos"}), 400

    Proveedor.add_proveedor(data)
    return jsonify({"message": "Proveedor creado exitosamente"}), 201

@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    """Actualiza un proveedor existente."""
    data = request.json
    if not Proveedor.validate(data):
        return jsonify({"message": "Datos inválidos"}), 400

    try:
        Proveedor.update_proveedor(id, data)
        return jsonify({"message": "Proveedor actualizado exitosamente"}), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404

@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    """Elimina un proveedor por su ID."""
    try:
        Proveedor.delete_proveedor(id)
        return jsonify({"message": "Proveedor eliminado exitosamente"}), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
