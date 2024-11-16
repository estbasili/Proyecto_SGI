from flask import Blueprint, request, jsonify
from models.proveedor import Proveedor
from models.producto import Producto
#from api import app

proveedor_bp = Blueprint('proveedor', __name__)

import logging

@proveedor_bp.route('/listarProveedores', methods=['GET'])
def get_all_list_proveedores():
    try:
        proveedores = Proveedor.get_all_list_proveedor()
        return jsonify(proveedores), 200
    except Exception as e:
        logging.error(f"Error al listar proveedores: {e}")
        return jsonify({"error": str(e)}), 400


@proveedor_bp.route('/proveedores', methods=['GET'])
def get_all_proveedores():
    try:
        proveedores = Proveedor.get_all_proveedores()
        if proveedores:
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
        #return jsonify({"mensaje": "Proveedor no encontrado"}), 404
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
    
  

@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos', methods=['POST'])
def asociar_producto_a_proveedor(id_proveedor):
    try:
        data = request.get_json()
        id_producto = data.get("id_producto")
        if not id_producto:
            return jsonify({"error": "ID de producto es necesario"}), 400
        resultado = Proveedor.asociar_producto(id_proveedor, id_producto)
        return jsonify(resultado), 201
    except Exception as e:
        logging.error(f"Error al asociar producto a proveedor: {e}")
        return jsonify({"error": str(e)}), 400

########################  modificacion para asociar varios productos #####################

@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos/varios', methods=['POST'])
def asociar_varios_productos_a_proveedor(id_proveedor):
    try:
        data = request.get_json()
        productos = data.get("productos", [])
        if not productos:
            return jsonify({"error": "Lista de productos es necesaria"}), 400
        resultado = Proveedor.asociar_varios_productos(id_proveedor, productos)
        return jsonify(resultado), 201
    except Exception as e:
        logging.error(f"Error al asociar varios productos a proveedor: {e}")
        return jsonify({"error": str(e)}), 400
    
##########################################################################################

    
# Obtener productos de un proveedor

@proveedor_bp.route('/proveedores/<int:id_proveedor>/productos', methods=['GET'])
def obtener_productos_de_proveedor(id_proveedor):
    try:
        productos = Proveedor.obtener_productos_con_proveedor(id_proveedor)  # Corregido el nombre del método
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500  # Error interno del servidor


