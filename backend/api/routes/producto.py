from flask import Blueprint, request, jsonify
from models.producto import Producto

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/pruebita', methods=['GET'])
def pruebita():
    return jsonify({"message": "Esto es una prueba"})


@producto_bp.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    if not Producto.validar_datos(data):
        return jsonify({"message": "Datos de producto inválidos"}), 400

    Producto.create(data)
    return jsonify({'message': 'Producto creado', 'producto': data}), 201


@producto_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.get_all()
    return jsonify(productos), 200


@producto_bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404
    return jsonify(producto.a_json()), 200


@producto_bp.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404

    if not Producto.validar_datos(data):
        return jsonify({"message": "Datos de producto inválidos"}), 400

    Producto.update(id, data)
    return jsonify({'message': 'Producto actualizado', 'producto': data}), 200


@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404

    Producto.delete(id)
    return jsonify({'message': 'Producto eliminado'}), 204
