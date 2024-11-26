from api.db.db import get_db_connection, DBError
from datetime import datetime, date
from api.models.detalle_orden import DetalleOrden
class Orden:
    schema = {
        "fecha_pedido": str,
        "fecha_recepcion": (str, type(None)),  # Permitir None como tipo válido
        "estado": int,  # Estado debe ser un entero
        "id_proveedor": int,
        #"id_usuario": int  # Si no lo usas, lo dejas comentado
    }

    @classmethod
    def validar_datos(cls, data):
        if data is None or not isinstance(data, dict):
            return False, "Error: Los datos no son un diccionario o son None."

        for key in cls.schema:
            if key not in data:
                return False, f"Error: Falta el campo '{key}' en los datos proporcionados."

            expected_types = cls.schema[key]

            # Validar tipo de dato
            if not isinstance(data[key], expected_types):
                return False, f"Error: El campo '{key}' tiene un valor de tipo inválido. Esperado: {expected_types}, Recibido: {type(data[key])}. Valor: {data[key]}"

            # Validar formato de las fechas
            if key in ["fecha_pedido", "fecha_recepcion"] and data[key] is not None:
                try:
                    datetime.strptime(data[key], '%Y-%m-%d')  # Verifica el formato
                except ValueError:
                    return False, f"Error: El campo '{key}' tiene un formato de fecha inválido. Valor recibido: {data[key]}"

        return True, "Validación exitosa. Todos los datos son válidos."

    def __init__(self, data):
        # Asignación de valores considerando el tipo adecuado
        self.id_orden = data[0]
        self.fecha_pedido = data[1] if isinstance(data[1], (datetime, date)) else datetime.strptime(data[1], '%Y-%m-%d') if data[1] else None
        self.fecha_recepcion = data[2] if isinstance(data[2], (datetime, date)) else datetime.strptime(data[2], '%Y-%m-%d') if data[2] else None
        self.estado = int(data[3])  # Convertir estado a entero
        self.id_proveedor = data[4]
        self.id_usuario = data[5] if len(data) > 5 else None  # Asegurar que no cause error si no existe


    def a_json(self):
        return {
            "id_orden": self.id_orden,
            "fecha_pedido": self.fecha_pedido.strftime('%Y-%m-%d') if self.fecha_pedido else None,
            "fecha_recepcion": self.fecha_recepcion.strftime('%Y-%m-%d') if self.fecha_recepcion else None,
            "estado": self.estado,
            "id_proveedor": self.id_proveedor,
           # "id_usuario": self.id_usuario
        }

    @classmethod
    def get_all_ordenes(cls,id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM orden_compra WHERE id_usuario = %s', (id_usuario,))
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if len(data)>0:
            lista = []
            for fila in data:
                objeto = Orden(fila).a_json()
                lista.append(objeto)
            return lista
        raise DBError("No existe el recurso solicitado")


    @classmethod
    def get_orden_by_id(cls, id, id_usuario):
        conexion = None
        cursor = None
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute(
                '''
                SELECT detalle_orden.id_orden, detalle_orden.id_producto, producto.nombre, detalle_orden.cantidad 
                FROM gestion_inventario.orden_compra 
                INNER JOIN detalle_orden ON detalle_orden.id_orden = orden_compra.id_orden
                INNER JOIN producto ON producto.id_producto = detalle_orden.id_producto
                WHERE orden_compra.id_orden = %s AND orden_compra.id_usuario = %s
                ''', (id, id_usuario)
            )
            data = cursor.fetchall()

            if not data:
                return False

            detalle_orden = [
                {"id_orden": row[0], "id_producto": row[1], "nombre": row[2], "cantidad": row[3]}
                for row in data
            ]

            return detalle_orden

        except Exception as e:
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    @classmethod
    def create_orden(cls, data, id_usuario):
        if not cls.validar_datos(data)[0]:
            raise ValueError("Datos inválidos")
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO orden_compra (fecha_pedido, fecha_recepcion, estado, id_proveedor, id_usuario)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (data['fecha_pedido'], data['fecha_recepcion'], data['estado'], data['id_proveedor'], id_usuario)
            )
            conexion.commit()
            id_orden = cursor.lastrowid
            return {"mensaje": "Orden creada exitosamente", "id_orden": id_orden, "error": False}
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al crear orden: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

    @classmethod
    def update_orden_by_id(cls, id, data, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            fecha_recepcion = data.get('fecha_recepcion')
            if not fecha_recepcion:
                fecha_recepcion = None

            cursor.execute(
                '''
                UPDATE orden_compra
                SET fecha_pedido = %s, fecha_recepcion = %s, estado = %s, id_proveedor = %s, id_usuario = %s
                WHERE id_orden = %s AND id_usuario = %s
                ''',
                (data['fecha_pedido'], fecha_recepcion, data['estado'], data['id_proveedor'], id_usuario, id, id_usuario)
            )
            conexion.commit()
            if cursor.rowcount == 0:
                return None
            return {"message": "Orden de compra actualizada exitosamente"}
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al actualizar orden: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

    @classmethod
    def delete_orden_by_id(cls, id, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM orden_compra WHERE id_orden = %s AND id_usuario = %s', (id, id_usuario))
            conexion.commit()
            if cursor.rowcount == 0:
                return None
            return True
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al eliminar orden: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
