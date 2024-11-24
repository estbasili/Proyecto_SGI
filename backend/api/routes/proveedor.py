from api import app
from flask import request, jsonify
from api.db.db import DBError
from api.models.proveedor import Proveedor
from api.models.producto import Producto

#obtener todos los proveedores por uusario
@app.route('/usuarios/<int:id_usuario>/proveedores', methods=['GET'])
def get_proveedores_by_user(id_usuario):
    try:
        proveedores = Proveedor.get_proveedores_by_user(id_usuario)
        if proveedores:
            return jsonify(proveedores), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    
#Crear un nuevo proveedor por usuario
@app.route('/usuarios/<int:id_usuario>/proveedores', methods=['POST'])
def create_proveedor_by_user(id_usuario):
    try:
        data = request.get_json() 
        proveedores = Proveedor.create_proveedor_by_user(data, id_usuario)
        return jsonify(proveedores), 201
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    
# Actualizar un proveedor por ID
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_proveedor>', methods=['PUT'])
def update_proveedor_by_user(id_usuario, id_proveedor):
    try:
        data = request.get_json()
        proveedor = Proveedor.update_proveedor_by_user(data, id_usuario, id_proveedor)
        if proveedor:
            return jsonify(proveedor), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    
# Eliminar un proveedor por ID
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_proveedor>', methods=['DELETE'])
def delete_proveedor_by_user(id_usuario, id_proveedor):
    try:
        proveedor = Proveedor.delete_proveedor_by_user(id_usuario, id_proveedor)
        return jsonify(proveedor), 200
    except DBError as e:
        return jsonify({"mensaje": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#listar proveedores
@app.route('/usuarios/<int:id_usuario>/listarProveedores', methods=['GET']) 
def get_all_list_proveedores(id_usuario): 
    try:
        proveedores = Proveedor.get_all_list_proveedor(id_usuario)
        return jsonify(proveedores), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
    
# Obtener un proveedor por id_proveedor según el usuario
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_proveedor>', methods=['GET'])
def get_proveedor_by_id_proveedor(id_usuario, id_proveedor):
    try:
        proveedor = Proveedor.get_proveedor_by_id_proveedor(id_usuario, id_proveedor)
        return jsonify(proveedor), 200  
    except DBError as e:
        return jsonify({"message": str(e)}), 404  
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500  
    
#obtener productos asociados
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_proveedor>/productos', methods=['GET'])
def obtener_productos_con_proveedor(id_usuario, id_proveedor):
    try:
        productos = Proveedor.obtener_productos_con_proveedor(id_usuario, id_proveedor)
        return jsonify(productos), 200  
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500 

#asociar productos
@app.route('/usuarios/<int:id_usuario>/proveedores/<int:id_proveedor>/productos/varios', methods=['POST'])
def asociar_varios_productos_a_proveedor(id_usuario, id_proveedor):
    try:
        data = request.get_json()
        productos = data.get("productos", [])
        if not productos:
            return jsonify({"message": "Lista de productos es necesaria"}), 400
        resultados = []  
        for id_producto in productos:
            try:
                resultado = Proveedor.asociar_producto(id_usuario, id_proveedor, id_producto)
                resultados.append(resultado) 
            except Exception as e:
                resultados.append({
                    "id_producto": id_producto,
                    "error": str(e)
                })
        return jsonify({"resultados": resultados}), 201
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
