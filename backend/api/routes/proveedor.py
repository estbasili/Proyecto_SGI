from flask import Blueprint, request, jsonify
from db.db import DBError
from models.proveedor import Proveedor
from models.producto import Producto

proveedor_bp = Blueprint('proveedor', __name__)

@proveedor_bp.route('/listarProveedores', methods=['GET'])
def get_all_list_proveedores():
    try:
        proveedores = Proveedor.get_all_list_proveedor()
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@proveedor_bp.route('/proveedores', methods=['GET'])
def get_all_proveedores():
    try:
        proveedores = Proveedor.get_all_proveedores()
        if proveedores:
            return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Obtener un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = Proveedor.get_proveedor_by_id(id)
        if proveedor:
            return jsonify(proveedor), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
# Crear un nuevo proveedor
@proveedor_bp.route('/proveedores', methods=['POST'])
def create_proveedor():
    try:
        data = request.get_json()
        proveedor = Proveedor.create_proveedor(data)
        return jsonify(proveedor), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
# Actualizar un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        proveedor = Proveedor.update_proveedor(id, data)
        if proveedor:
            return jsonify(proveedor), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Eliminar un proveedor por ID
@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        proveedor = Proveedor.delete_proveedor(id)
        return jsonify(proveedor), 200
    except DBError as e:
        return jsonify({"mensaje": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos', methods=['POST'])
def asociar_producto_a_proveedor(id_proveedor):
    try:
        data = request.get_json()
        id_producto = data.get("id_producto")
        if not id_producto:
            return jsonify({"message": "ID de producto es necesario"}), 400
        resultado = Proveedor.asociar_producto(id_proveedor, id_producto)
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Modificación para asociar varios productos
@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos/varios', methods=['POST'])
def asociar_varios_productos_a_proveedor(id_proveedor):
    try:
        data = request.get_json()
        productos = data.get("productos", [])
        if not productos:
            return jsonify({"message": "Lista de productos es necesaria"}), 400
        resultado = Proveedor.asociar_varios_productos(id_proveedor, productos)
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Obtener productos de un proveedor
@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos', methods=['GET'])
def obtener_productos_de_proveedor(id_proveedor):
    try:
        productos = Proveedor.obtener_productos_con_proveedor(id_proveedor)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"message": f"message interno: {str(e)}"}), 500
