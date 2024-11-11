from db.db import get_db_connection, DBError
from datetime import datetime

class Orden:
    schema = {
        "fecha_pedido": str,
        "fecha_recepcion": (str, type(None)),  # Permitir None como tipo válido
        "estado": str,
        "id_proveedor": int,
        "id_usuario": int
    }

    @classmethod
    def validar_datos(cls, data):
        if data is None or not isinstance(data, dict):
            return False
        for key in cls.schema:
            if key not in data:
                return False
            # Verificamos que el valor del campo coincida con el tipo esperado
            expected_types = cls.schema[key]
            if not isinstance(data[key], expected_types):
                return False
        return True


    def __init__(self, data):
        self.id_orden = data[0]
        self.fecha_pedido = data[1]
        self.fecha_recepcion = data[2]
        self.estado = data[3]
        self.id_proveedor = data[4]
        self.id_usuario = data[5]

    
    def a_json(self):
        return {
            "id_orden": self.id_orden,
            "fecha_pedido": self.fecha_pedido.strftime('%Y-%m-%d') if self.fecha_pedido else None,
            "fecha_recepcion": self.fecha_recepcion.strftime('%Y-%m-%d') if self.fecha_recepcion else None,
            "estado": self.estado,
            "id_proveedor": self.id_proveedor,
            "id_usuario": self.id_usuario
        }

    @classmethod
    def get_all_ordenes(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM orden_compra')
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [Orden(orden).a_json() for orden in data]
    
    @classmethod
    def get_orden_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM orden_compra WHERE id_orden = %s', (id,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        return Orden(data).a_json() if data else None
    

    @classmethod
    def create_orden(cls,data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
             # Si 'fecha_recepcion' no está presente o es una cadena vacía, asignamos None
            fecha_recepcion = data.get('fecha_recepcion')
            if fecha_recepcion in [None, "", "-"]:  # Manejar None, cadena vacía y "-"
              fecha_recepcion = None

            cursor.execute(
                 'INSERT INTO orden_compra (fecha_pedido, fecha_recepcion, estado, id_proveedor, id_usuario) VALUES (%s, %s, %s, %s, %s)',
            (data['fecha_pedido'], fecha_recepcion, data['estado'], data['id_proveedor'], data['id_usuario'])
            )
            conexion.commit()
            return {"message": "orden de compra creada exitosamente"}, 201
        except Exception as e:
            conexion.rollback()
            raise Exception(f'Error al crear orden: {str(e)}')
        finally:
            cursor.close()
            conexion.close()


    @classmethod
    def update_orden_by_id(cls, id, data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            fecha_recepcion = data.get('fecha_recepcion')
            if not fecha_recepcion:  # Si es None o cadena vacía
                fecha_recepcion = None

            cursor.execute(
                '''
                UPDATE orden_compra
                SET fecha_pedido = %s, fecha_recepcion = %s, estado = %s, id_proveedor = %s, id_usuario = %s
                WHERE id_orden = %s
                ''',
                (data['fecha_pedido'], fecha_recepcion, data['estado'], data['id_proveedor'], data['id_usuario'], id)
            )
            conexion.commit()
            if cursor.rowcount == 0:
                return None  # No se encontró la orden
            return {"message": "Orden de compra actualizada exitosamente"}
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al actualizar orden: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    @classmethod
    def delete_orden_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM orden_compra WHERE id_orden = %s', (id,))
            conexion.commit()
            if cursor.rowcount == 0:
                return None  # No se encontró la orden
            return True
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al eliminar orden: {str(e)}")
        finally:
            cursor.close()
            conexion.close()