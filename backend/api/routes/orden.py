from api import app
from flask import request, jsonify
from api.models.orden import Orden
import sys
from api.models.detalle_orden import DetalleOrden
from api.utils.security import token_required
from api.db.db import DBError

# Obtener todas las órdenes
@app.route('/usuarios/<int:id_usuario>/ordenes', methods=['GET'])
#token_required
def get_all_ordenes(id_usuario):
    try:
        ordenes = Orden.get_all_ordenes(id_usuario)
        return jsonify(ordenes), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500

@app.route('/usuarios/<int:id_usuario>/ordenes/<int:id>', methods=['GET'])
#@token_required
def get_orden_by_id(id_usuario, id):
    try:
        # Obtener la orden del usuario especificado
        orden = Orden.get_orden_by_id(id, id_usuario)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/usuarios/<int:id_usuario>/ordenes', methods=['POST'])
@token_required
def create_orden(id_usuario):
    try:
        # Captura el JSON enviado
        data = request.get_json()

        # Validar que se haya recibido algo
        if data is None:
            return jsonify({"error": True, "message": "No se recibió un JSON válido."}), 400

        # Validar los datos
        is_valid, validation_message = Orden.validar_datos(data)
        if not is_valid:
            return jsonify({"error": True, "message": validation_message}), 202

        # Procesar 'productos'
        productos = data.get('productos', None)
        if 'productos' in data:
            del data['productos']

        if productos is None or not isinstance(productos, list):
            return jsonify({"error": True, "message": "El campo 'productos' es obligatorio y debe ser una lista."}), 400

        # Validar productos
        renglones_validos, mensaje = DetalleOrden.validar_datos(productos, id_usuario)
        if not renglones_validos:
            return jsonify({"error": True, "message": mensaje}), 202

        # Crear la orden
        orden = Orden.create_orden(data, id_usuario)
        if not orden:
            return jsonify({"error": True, "message": "No se pudo crear la orden."}), 500

        id_orden_creada = orden["id_orden"]

        # Crear el detalle de la orden
        detalle = DetalleOrden.createDetalleOrden(id_orden_creada, productos,id_usuario)

        # Respuesta exitosa
        return jsonify({"success": True, "message": "Orden creada con éxito", "orden": orden}), 201

    except Exception as e:
        # Registra el error para identificar la causa
        return jsonify({"error": str(e)}), 400



@app.route('/usuarios/<int:id_usuario>/ordenes/<int:id>', methods=['PUT'])
@token_required
def update_orden_by_id(id_usuario, id):
    try:
        data = request.get_json()

        # Validar los datos
        if not Orden.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400

        # Actualizar la orden
        orden = Orden.update_orden_by_id(id, data, id_usuario)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/usuarios/<int:id_usuario>/ordenes/<int:id>', methods=['DELETE'])
@token_required
def delete_orden_by_id(id_usuario, id):
    try:
        # Eliminar la orden
        result = Orden.delete_orden_by_id(id, id_usuario)
        if result:
            return jsonify({"mensaje": "Orden eliminada exitosamente"}), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


