from db.db import get_db_connection, DBError
from models.producto import Producto
import logging #########################################################################################

# Configuración de logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')############

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
        if len(data)>0:
            proveedores = [Proveedor(proveedor).json_select() for proveedor in data]
            return proveedores
        raise DBError("No existe el recurso solicitado")
    
    
    @classmethod
    def get_all_proveedores(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall() #Cada elemento de data es una tupla con los valores de una fila de la tabla proveedor
        cursor.close()
        conexion.close()
        if data is not None:
            proveedores = [Proveedor(proveedor).a_json() for proveedor in data]
            return proveedores
        raise DBError("No existe el recurso solicitado")

    @classmethod
    def get_proveedor_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
            data = cursor.fetchone()
            if data is not None:
                return Proveedor(data).a_json()
            raise DBError('No existe el recurso solicitado')
        except Exception as e:
            raise Exception(f"Error al obtener proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    #chequear lo de id_usuario
    @classmethod
    def create_proveedor(cls, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES (%s, %s, %s, %s)',
                (data['nombre'], data['telefono'], data['email'], data['id_usuario'])
            )
            conexion.commit()
             # Obtener el ID del proveedor recién creado
            id_proveedor = cursor.lastrowid
            return {"mensaje": "Proveedor creado exitosamente","id_proveedor":id_proveedor}, 201 ################################## se modifico para que devuelva el id_proveeedor ultimo creado
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Error al crear proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
    
    @classmethod
    def update_proveedor(cls, id, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Control si existe el recurso
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe el recurso solicitado")
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
        # Control si existe el recurso
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe el recurso solicitado")
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

    #@classmethod
    #def asociar_producto(cls, id_proveedor, id_producto):
    #    conexion = get_db_connection()
    #    cursor = conexion.cursor()
    #    try:
    #        cursor.execute(
    #            'INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES (%s, %s)',
    #            (id_proveedor, id_producto)
    #        )
    #        conexion.commit()
    #        return {"mensaje": "Producto asociado al proveedor exitosamente"}
    #    except Exception as e:
    #        conexion.rollback()
    #        raise Exception(f"Error al asociar producto con proveedor: {str(e)}")
    #    finally:
    #        cursor.close()
    #        conexion.close()

    
    @classmethod
    def asociar_producto(cls, id_proveedor, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Verificar si el proveedor existe
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Proveedor con ID {id_proveedor}")
        
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Producto con ID {id_producto}")
        try:
            # Inserción en la tabla intermedia proveedor_producto
            cursor.execute("INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES (%s, %s)", (id_proveedor, id_producto))
            conexion.commit()
            return {"id_proveedor": id_proveedor, "id_producto": id_producto, "estado": "asociado"}
        except Exception as e:
            logging.error(f"Error al asociar producto: {e}")
            return {"error": str(e)}
        finally:
            cursor.close()
            conexion.close()

    @classmethod
    def asociar_varios_productos(cls, id_proveedor, productos):
        try:
            for id_producto in productos:
                cls.asociar_producto(id_proveedor, id_producto)
            return {"mensaje": "Productos asociados correctamente"}
        except Exception as e:
            logging.error(f"Error al asociar varios productos: {e}")
            return {"error": str(e)}
    
    @classmethod
    def obtener_productos(cls, id_proveedor):
        conexion = get_db_connection()
        cursor = conexion.cursor()
         # Verificar si el proveedor existe
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        if cursor.fetchone() is None:
            raise DBError(f"No existe el recurso solicitado: Proveedor con ID {id_proveedor}")
        try:
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
        
        # Obtengo el nombre y el id del producto
            productos = [(producto[0], producto[1]) for producto in cursor.fetchall()]
            return productos
        except Exception as e:
            raise Exception(f"Error al obtener productos del proveedor: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

