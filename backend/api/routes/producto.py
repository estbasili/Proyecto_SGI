from api import app
from flask import request, jsonify
from api.models.producto import Producto
from api.models.proveedor import Proveedor


@app.route('/pruebita', methods=['GET'])
def pruebita():
    return jsonify({"message": "Esto es una prueba"})


@app.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    if not Producto.validar_datos(data):
        return jsonify({"message": "Datos de producto inválidos"}), 400

    Producto.create(data)
    return jsonify({'message': 'Producto creado', 'producto': data}), 201


@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.get_all()
    return jsonify(productos), 200


@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404
    return jsonify(producto.a_json()), 200


@app.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404

    if not Producto.validar_datos(data):
        # Agrega detalles del error en la validación para más claridad
        return jsonify({"message": "Datos de producto inválidos", "error": "Datos mal formateados o faltantes"}), 400

    Producto.update(id, data)
    return jsonify({'message': 'Producto actualizado', 'producto': data}), 200

#@app.route('/productos/<int:id>', methods=['PUT'])
#def update_producto(id):
#    data = request.get_json()
#    producto = Producto.get_by_id(id)
#    if producto is None:
#        return jsonify({'message': 'Producto no encontrado'}), 404

#    if not Producto.validar_datos(data):
#        return jsonify({"message": "Datos de producto inválidos"}), 400

#    Producto.update(id, data)
#    return jsonify({'message': 'Producto actualizado', 'producto': data}), 200


@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    #print(type(id))
    producto = Producto.get_by_id(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404

    Producto.delete(id)
    return jsonify({'message': 'Producto eliminado'}), 204

@app.route('/productos/<int:id>/proveedores', methods=['GET'])
def get_proveedores_por_producto(id):
    proveedores = Producto.get_proveedores(id)
    if not proveedores:
        return jsonify({"message": "No se encontraron proveedores para este producto"}), 404
    return jsonify(proveedores), 200

##################################################################
# ruta: /productos/id_usuario/proveedores que recibe el id_ usuario_sesion y devuelva un arreglo de dict
# [{"id_producto": , "producto_nombre": ,"proveedor_nombre": "stock": }, {...}, ... ] para ser representado en una tabla
# en la parte de inventario actual del frontend
@app.route('/productos/<int:id_usuario>/usuario', methods=['GET'])
def usuario_productos_proveedores(id_usuario):
    productos = Producto.get_productos_proveedores(id_usuario)
    if not productos :
        return jsonify({'message': 'Productos no encontrado'}), 404
    return jsonify(productos), 200
#################################################################33
