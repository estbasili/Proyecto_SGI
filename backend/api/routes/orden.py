from api import app
from flask import request, jsonify
from api.models.orden import Orden
import sys
from api.models.detalle_orden import DetalleOrden
# Obtener todas las órdenes
@app.route('/ordenes', methods=['GET'])
def get_all_ordenes():
    try:
        ordenes = Orden.get_all_ordenes()
        return jsonify(ordenes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

# Obtener una orden por ID
@app.route('/ordenes/<int:id>', methods=['GET'])
def get_orden_by_id(id):
    try:
        orden = Orden.get_orden_by_id(id)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/ordenes', methods=['POST'])
def create_orden():
        # Captura el JSON enviado
        data = request.get_json()
        print("Datos recibidos en el servidor:", data)  # Log para depuración

        # Validar los datos (simulación de función de validación)
        is_valid, validation_message = Orden.validar_datos(data)
        if not is_valid:
            print('Datos inválidos antes de continuar')
            return jsonify({"error": True, "message": validation_message}), 400

        # Guardar el valor de 'productos' en una variable, y eliminarlo del cuerpo
        productos = data.get('productos', None)
        if 'productos' in data:
            del data['productos']

        # Verificar si los productos existen y son válidos
        if productos is None or not isinstance(productos, list):
            return jsonify({"error": True, "message": "El campo 'productos' es obligatorio y debe ser una lista."}), 400

        # Validar los productos en los renglones de la orden
        renglones_validos, mensaje = DetalleOrden.validar_datos(productos)
        if not renglones_validos:
            return jsonify({"error": True, "message": mensaje}), 202

        # Crear la orden si los datos son válidos
        orden = Orden.create_orden(data)
        id_orden_creada = orden["id_orden"]
        
        #sys.exit()
        
        
        detalle = DetalleOrden.createDetalleOrden(id_orden_creada,productos)
        
        if not orden:
            return jsonify({"error": True, "message": "No se pudo crear la orden."}), 500

        # Respuesta exitosa con los datos de la orden creada
        return jsonify({"success": True, "message": "Orden creada con éxito", "orden": orden}), 201



    

# Actualizar una orden existente
@app.route('/ordenes/<int:id>', methods=['PUT'])
def update_orden_by_id(id):
    try:
        data = request.get_json()
        if not Orden.validar_datos(data):
            return jsonify({"error": "Datos inválidos"}), 400
        orden = Orden.update_orden_by_id(id, data)
        if orden:
            return jsonify(orden), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Eliminar una orden
@app.route('/ordenes/<int:id>', methods=['DELETE'])
def delete_orden_by_id(id):
    try:
        result = Orden.delete_orden_by_id(id)
        if result:
            return jsonify({"mensaje": "Orden eliminada exitosamente"}), 200
        return jsonify({"mensaje": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400