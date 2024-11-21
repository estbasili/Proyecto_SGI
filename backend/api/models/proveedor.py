from api.db.db import get_db_connection, DBError
from api.models.producto import Producto
from contextlib import closing
import logging
# Configuración de logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Proveedor:
    schema = {
        "nombre": str,
        "telefono": str, 
        "email": str,
        "id_usuario": int,
    }

    @classmethod
    def validar_datos(cls, data):
        if data is None or type(data) != dict:
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

    def json_select(self):
        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
        }

    @classmethod
    def get_all_list_proveedor(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if len(data) > 0:
            return [Proveedor(proveedor).json_select() for proveedor in data]
        raise DBError("No existe el recurso solicitado")
    
    @classmethod
    def get_all_proveedores(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if data:
            return [Proveedor(proveedor).a_json() for proveedor in data]
        raise DBError("No existe el recurso solicitado")

    @classmethod
    def get_proveedor_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if data:
            return Proveedor(data).a_json()
        raise DBError('No existe el recurso solicitado')

    @classmethod
    def create_proveedor(cls, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Control si el email no esta en uso por otro proveedor
        email = data["email"]
        cursor.execute('SELECT * FROM proveedor WHERE email = %s', (email,))
        row = cursor.fetchone()
        if row is not None:
            raise DBError("Email ya registrado")
        
        cursor.execute(
            'INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES (%s, %s, %s, %s)',
            (data['nombre'], data['telefono'], data['email'], data['id_usuario'])
        )
        conexion.commit()
        id_proveedor = cursor.lastrowid
        cursor.close()
        conexion.close()
        return {"mensaje": "Proveedor creado exitosamente", "id_proveedor": id_proveedor}

    @classmethod
    def update_proveedor(cls, id, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute(
            'UPDATE proveedor SET nombre = %s, telefono = %s, email = %s, id_usuario = %s WHERE id_proveedor = %s',
            (data['nombre'], data['telefono'], data['email'], data['id_usuario'], id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje: Proveedor actualizado"}

    @classmethod
    def delete_proveedor(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute('DELETE FROM proveedor WHERE id_proveedor = %s', (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Proveedor eliminado"}

    @classmethod
    def asociar_producto(cls, id_proveedor, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Proveedor con ID {id_proveedor}")
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Producto con ID {id_producto}")
        cursor.execute("INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES (%s, %s)", (id_proveedor, id_producto))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"id_proveedor": id_proveedor, "id_producto": id_producto, "estado": "asociado"}

    @classmethod
    def obtener_productos_con_proveedor(cls, id_proveedor):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Proveedor con ID {id_proveedor}")
        cursor.execute(
            '''
            SELECT 
            producto.id_producto as idProducto ,
            producto.nombre as nombre_producto
            FROM proveedor
            INNER JOIN producto_proveedor 
            on proveedor.id_proveedor = producto_proveedor.id_proveedor
            INNER JOIN producto 
            on producto_proveedor.id_producto = producto.id_producto 
            Where proveedor.id_proveedor = %s 
            ''', 
            (id_proveedor,)
        )
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if not data:
            raise DBError("No existen productos asociados al proveedor solicitado.")
        return [{"idProducto": row[0], "nombre_producto": row[1]} for row in data]
