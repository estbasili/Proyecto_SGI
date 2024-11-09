from db.db import get_db_connection, DBError

class Proveedor:
    schema = {
        "nombre": str,
        "telefono": str,
        "email": str,
        "id_usuario": int,
    }

    @classmethod
    def validar_datos(cls,data):
        if data == None or type(data) != dict:
            return False
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto?
            if type(data[key]) != cls.schema[key]: 
                return False
        return True

    def __init__(self, data):
        self.id_proveedor = data[0]
        self.nombre = data[1]
        self.telefono = data[2]
        self.email = data[3]
        self.id_usuario = data[4]

    def a_json(self):
        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "id_usuario": self.id_usuario
        }

    
    @classmethod
    def get_all_proveedores(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall()
        cursor.close()
        conexion.close()

        proveedores = [Proveedor(proveedor).a_json() for proveedor in data]
        return proveedores

    @classmethod
    def get_proveedor_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
            data = cursor.fetchone()
            if data:
                return Proveedor(data).a_json()
            return None
        except Exception as e:
            raise Exception(f"Error al obtener proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    #chequear lo de id_usuario
    @classmethod
    def create_proveedor(cls, data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES (%s, %s, %s, %s)',
                (data['nombre'], data['telefono'], data['email'], data['id_usuario'])
            )
            conexion.commit()
            return {"mensaje": "Proveedor creado exitosamente"}, 201
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al crear proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    @classmethod
    def update_proveedor(cls, id, data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE proveedor SET nombre = %s, telefono = %s, email = %s, id_usuario = %s WHERE id_proveedor = %s',
                (data['nombre'], data['telefono'], data['email'], data['id_usuario'], id)
            )
            conexion.commit()
            if cursor.rowcount > 0:
                return cls.get_proveedor_by_id(id)
            return None
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al actualizar proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

    @classmethod
    def delete_proveedor(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM proveedor WHERE id_proveedor = %s', (id,))
            conexion.commit()
            if cursor.rowcount > 0:
                return {"mensaje": "Proveedor eliminado"}
            return None
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al eliminar proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()