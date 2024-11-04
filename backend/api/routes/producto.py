from flask import Blueprint, request, jsonify
import mysql.connector
from db.db import get_db_connection

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/pruebita', methods=['GET'])
def pruebita():
    return jsonify({"message": "Esto es una prueba"})


# Obtener todos los productos
#@producto_bp.route('/productos', methods=['GET'])
#def get_productos():
    #connection = get_db_connection()
    #cursor = connection.cursor()
    #cursor.execute("SELECT * FROM producto")
    #productos = cursor.fetchall()
    #cursor.close()
    #connection.close()

    # Convertir los resultados a un formato JSON
    #productos_list = [
        #{'id': p[0], 'nombre': p[1], 'descripcion': p[2], 'precio': p[3], 'stock': p[4]}
        #for p in productos
    #]
    #return jsonify(productos_list), 200

# Crear un nuevo producto
@producto_bp.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data.get('descripcion')
    precio = data['precio']
    stock = data.get('stock', 0)

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, precio, stock)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Producto creado', 'producto': {'nombre': nombre}}), 201

# Actualizar un producto existente
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    stock = data.get('stock')

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    if not producto:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Actualizar producto
    cursor.execute(
        "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id = %s",
        (nombre or producto[1], descripcion or producto[2], precio or producto[3], stock or producto[4], id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Producto actualizado', 'producto': {'id': id, 'nombre': nombre or producto[1]}}), 200

# Eliminar un producto existente
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    if not producto:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Eliminar producto
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Producto eliminado'}), 204
