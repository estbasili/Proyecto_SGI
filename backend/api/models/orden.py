from api.db.db import get_db_connection, DBError
from datetime import datetime, date

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
        self.id_orden = data[0]
        self.fecha_pedido = data[1] if isinstance(data[1], (datetime, date)) else datetime.strptime(data[1], '%Y-%m-%d') if data[1] else None
        self.fecha_recepcion = data[2] if isinstance(data[2], (datetime, date)) else datetime.strptime(data[2], '%Y-%m-%d') if data[2] else None
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
    def create_orden(cls, data):
        print("LLEGO A LA CREACIÓN CON LOS DATOS:")
        print(data)

        if not cls.validar_datos(data):
            raise ValueError("Datos inválidos")

        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            # Ejecutar el INSERT
            cursor.execute(
                '''
                INSERT INTO orden_compra (fecha_pedido, fecha_recepcion, estado, id_proveedor, id_usuario)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (data['fecha_pedido'], data['fecha_recepcion'], data['estado'], data['id_proveedor'], data['id_usuario'])
            )
            # Confirmar la transacción
            conexion.commit()

            # Obtener el ID recién creado
            id_orden = cursor.lastrowid
            print(f"Orden creada con ID: {id_orden}")

            # Retornar un mensaje y el ID
            return {"mensaje": "Orden creada exitosamente", "id_orden": id_orden, "error": False}
        except Exception as e:
            # Revertir cambios en caso de error
            conexion.rollback()
            raise Exception(f"Error al crear orden: {str(e)}")
        finally:
            # Cerrar la conexión y el cursor
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