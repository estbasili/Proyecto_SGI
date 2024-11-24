from api import app
from flask import request, jsonify
from api.models.producto import Producto
from api.models.proveedor import Proveedor
from api.db.db import DBError


@app.route('/usuarios/<int:id_usuario>/productos', methods=['GET'])
def get_productos_por_usuario(id_usuario):
    try:
        productos = Producto.get_productos_by_user(id_usuario)
        return jsonify(productos), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    

@app.route('/usuarios/<int:id_usuario>/productos/<int:id_producto>', methods=['GET'])
def get_producto_por_id(id_usuario, id_producto):
    try:
        producto = Producto.get_by_id_producto(id_usuario, id_producto)
        return jsonify(producto), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado"}), 500
    
@app.route('/usuarios/<int:id_usuario>/productos', methods=['POST'])
def create_producto(id_usuario):
    data = request.get_json()
    try:
        productos = Producto.create_producto_by_user(data, id_usuario)
        return jsonify(productos), 201
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500


@app.route('/usuarios/<int:id_usuario>/productos/<int:id_producto>', methods=['PUT'])
def update_producto(id_usuario, id_producto):
    data = request.get_json()
    try:
        productos_actualizados = Producto.update_producto_by_user(data, id_usuario, id_producto)
        return jsonify(productos_actualizados), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    
@app.route('/usuarios/<int:id_usuario>/productos/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_usuario, id_producto):
    try:
        productos = Producto.delete_by_user(id_usuario,id_producto)
        return jsonify(productos), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    

    
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_producto>', methods=['GET'])
def obtener_proveedores(id_usuario, id_producto):
    try:
        proveedores = Producto.get_proveedores(id_usuario, id_producto)
        return jsonify(proveedores), 200  
    except DBError:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500


##################################################################
# ruta: /productos/id_usuario/proveedores que recibe el id_ usuario_sesion y devuelva un arreglo de dict
# [{"id_producto": , "producto_nombre": ,"proveedor_nombre": "stock": }, {...}, ... ] para ser representado en una tabla
# en la parte de inventario actual del frontend
@app.route('/usuarios/<int:id_usuario>/productos', methods=['GET'])
def usuario_productos_proveedores(id_usuario):
    try:
        productos = Producto.get_productos_proveedores(id_usuario)
        return jsonify(productos), 200
    except DBError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f"Error inesperado: {str(e)}"}), 500

