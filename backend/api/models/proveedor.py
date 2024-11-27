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
        #"id_usuario": int, ya no es necesario
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
            #"id_usuario": self.id_usuario esto ya no se necesita
        }

    def json_select(self):
        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
        }
  
    
    #metodo actuyalizado segun cada usuario
    @classmethod
    def get_proveedores_by_user(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_usuario = %s', (id_usuario,))
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        #Comprobar si se obtuvo algun registro
        if len(data)>0:
            lista = []
            for fila in data:
                objeto = Proveedor(fila).a_json()
                lista.append(objeto)
            return lista
        raise DBError("No existe el recurso solicitado")
    
    #Crear proveedor
    @classmethod
    def create_proveedor_by_user(cls, data, id_usuario):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT * FROM proveedor WHERE email = %s AND id_usuario = %s',
            (data["email"], id_usuario)
        )
        if cursor.fetchone():
            raise DBError("Email ya registrado")
        
        cursor.execute(
            '''
            INSERT INTO proveedor (nombre, telefono, email, id_usuario)
            VALUES (%s, %s, %s, %s)
            ''',
            (data["nombre"], data["telefono"], data["email"], id_usuario)
        )
        conexion.commit()
        #id_proveedor = cursor.lastrowid #t da el ultimo id generado
        cursor.close()
        conexion.close()
        return cls.get_proveedores_by_user(id_usuario)
        #return {"mensaje": "Proveedor creado exitosamente", "id_proveedor": id_proveedor}

    #Update proveedor
    @classmethod
    def update_proveedor_by_user(cls,data, id_usuario, id_proveedor):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id_proveedor,))
        proveedor = cursor.fetchone()
        if proveedor is None:
          raise DBError("No existe el recurso solicitado")
        if proveedor[4] != id_usuario:  # id_usuario está en la columna 4
            raise DBError("No tienes permiso para modificar este proveedor.")
        cursor.execute(
            'SELECT * FROM proveedor WHERE email = %s AND id_usuario = %s',
            (data["email"], id_usuario)
        )
        if cursor.fetchone():
            raise DBError("Email ya registrado")
        
        cursor.execute(
            'UPDATE proveedor SET nombre = %s, telefono = %s, email = %s, id_usuario = %s WHERE id_proveedor = %s',
            (data['nombre'], data['telefono'], data['email'], id_usuario, id_proveedor)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        #return {"mensaje: Proveedor actualizado"}
        return cls.get_proveedores_by_user(id_usuario)
    
    #delete
    @classmethod
    def delete_proveedor_by_user(cls, id_usuario, id_proveedor):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id_proveedor,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute('DELETE FROM proveedor WHERE id_proveedor = %s', (id_proveedor,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_proveedores_by_user(id_usuario)
        #return {"mensaje": "Proveedor eliminado"}


    @classmethod
    def get_all_list_proveedor(cls, id_usuario): 
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_usuario = %s', (id_usuario,))
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if len(data) > 0:
            return [Proveedor(proveedor).json_select() for proveedor in data]
        raise DBError("No existe el recurso solicitado")

    #Proveedor por id_proveedor
    @classmethod
    def get_proveedor_by_id_proveedor(cls, id_usuario, id_proveedor):
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute(
                'SELECT * FROM proveedor WHERE id_usuario = %s AND id_proveedor = %s',
                (id_usuario, id_proveedor)
            )
            data = cursor.fetchone()
            cursor.close()
            conexion.close()
            if data:
                return Proveedor(data).a_json()
            raise DBError('No existe el recurso solicitado')
        except Exception as e:
            raise DBError(f"Error al consultar proveedor: {str(e)}")

    
    @classmethod
    def obtener_productos_con_proveedor(cls, id_usuario, id_proveedor):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s AND id_usuario = %s",
                       (id_proveedor, id_usuario))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute(
        '''
        SELECT 
            producto.id_producto AS idProducto,
            producto.nombre AS nombre_producto
        FROM proveedor
        INNER JOIN producto_proveedor 
            ON proveedor.id_proveedor = producto_proveedor.id_proveedor
        INNER JOIN producto 
            ON producto_proveedor.id_producto = producto.id_producto
        WHERE proveedor.id_proveedor = %s
        ''', 
        (id_proveedor,))
        data = cursor.fetchall()
        cursor.close()
        conexion.close()
        if not data:
            raise DBError(f"No existen productos asociados al proveedor con ID {id_proveedor}.")
        return [{"idProducto": row[0], "nombre_producto": row[1]} for row in data]
    
    
    #asociar productos---- falta probarla, porque todavia no tengo listo lo de productos hasta ahora pide la lista pero no falla
    @classmethod
    def asociar_producto(cls, id_usuario, id_proveedor, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s AND id_usuario = %s", (id_proveedor, id_usuario))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado o no tienes permiso: Proveedor con ID {id_proveedor}")
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Producto con ID {id_producto}")
        cursor.execute("INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES (%s, %s)", (id_proveedor, id_producto))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"id_usuario": id_usuario, "id_proveedor": id_proveedor, "id_producto": id_producto, "estado": "asociado"}


