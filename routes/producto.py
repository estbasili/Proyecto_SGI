# routes/auth.py
from flask import Blueprint, request, jsonify
from models.producto import Producto

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/products/<int:id>', methods=['GET'])
def get_products_by_id(id):
    product = Producto.get_by_id(id)  # Llama al método para obtener el producto por ID
    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404  # Retorna un error 404 si no se encuentra el producto
    return jsonify(vars(product))  # Retorna el producto en formato JSON

@producto_bp.route('/products', methods=['GET'])
def get_all_products():
    #products = Producto.get_all()
    products = Producto.get_all_tabla()
    return jsonify([vars(product) for product in products]), 200  # Devuelve todos los productos en formato JSON
