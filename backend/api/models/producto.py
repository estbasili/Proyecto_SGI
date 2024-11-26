from api.db.db import get_db_connection, DBError

class Producto:
    schema = {
        "nombre": str,
        "descripcion": str,
        "precio": float,
        "stock": int,
        "id_categoria": int,
        #"id_usuario": int,
    }

    @classmethod
    def validar_datos(cls, data):
        if data is None or type(data) != dict:
            return False
        for key in cls.schema:
            if key not in data or type(data[key]) != cls.schema[key]:
                 return False
        return True

    def __init__(self, data):
        self.id_producto = data[0]
        self.nombre = data[1]
        self.descripcion = data[2]
        self.precio = data[3]
        self.stock = data[4]
        self.id_categoria = data[5]
        self.id_usuario = data[6]

    def a_json(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            #"id_usuario": self.id_usuario,
        }
    
    def json_select(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
        }

    @classmethod
    def get_productos_by_user(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT 
            producto.id_producto,
            producto.nombre AS producto_nombre,
            producto.descripcion,
            producto.precio,
            producto.stock,
            producto.id_categoria,
            categoria.nombre AS categoria_nombre
        FROM 
            producto
        INNER JOIN 
            categoria ON producto.id_categoria = categoria.id_categoria
        WHERE 
            producto.id_usuario = %s
        """, (id_usuario,))
        productos = []
        for producto in cursor.fetchall():
            productos.append({
            "id_producto": producto[0],
            "nombre": producto[1],
            "descripcion": producto[2],
            "precio": producto[3],
            "stock": producto[4],
            "id_categoria": producto[5],
            "categoria_nombre": producto[6]
            })
        cursor.close()
        conexion.close()
        #si no se encontraron productos
        #if not productos:
        #   raise DBError(f"No existen productos para el usuario con ID {id_usuario}")
        return productos
    
    #producto por id_producto
    @classmethod
    def get_by_id_producto(cls, id_usuario, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM producto WHERE id_usuario = %s AND id_producto = %s", (id_usuario, id_producto))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if data:
           return cls(data).a_json()  # Retornar datos en formato JSON
        return []


    #create
    @classmethod
    def create_producto_by_user(cls, data, id_usuario):
        if not cls.validar_datos(data):
            raise ValueError("Datos inválidos para crear el producto.")
        conexion = get_db_connection()
        cursor = conexion.cursor()
      #Verificar si ya existe un producto con el mismo nombre, categoría y usuario
        cursor.execute(
        """
        SELECT id_producto FROM producto 
        WHERE nombre = %s AND id_categoria = %s AND id_usuario = %s
        """,
        (data['nombre'], data['id_categoria'], id_usuario))
        producto_existente = cursor.fetchone()
        if producto_existente:
            cursor.close()
            conexion.close()
            raise DBError(f"El producto {data['nombre']} ya existe en la categoría {data['id_categoria']} para este usuario.")
        cursor.execute(
        """
        INSERT INTO producto (nombre, descripcion, precio, stock, id_categoria, id_usuario) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (data['nombre'], data['descripcion'], data['precio'], data['stock'], data['id_categoria'], id_usuario))
        conexion.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_producto = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return {"id_producto": id_producto, "mensaje": "Producto creado con éxito."}
    
    #update
    @classmethod
    def update_producto_by_user(cls, data, id_usuario, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
    # Verificar si el producto existe y pertenece al usuario
        cursor.execute(
        "SELECT id_usuario FROM producto WHERE id_producto = %s",
        (id_producto,))
        producto = cursor.fetchone()
        if producto is None:
            cursor.close()
            conexion.close()
            raise DBError("No existe el recurso solicitado")
        if producto[0] != id_usuario:
            cursor.close()
            conexion.close()
            raise DBError(f"No tienes permiso para actualizar este producto.")
        cursor.execute(
        "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s WHERE id_producto = %s AND id_usuario = %s",
        (data['nombre'], data['descripcion'], data['precio'], data['stock'], data['id_categoria'], id_producto, id_usuario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_productos_by_user(id_usuario)

    @classmethod
    def delete_by_user(cls, id_usuario, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario FROM producto WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        if producto is None:
            cursor.close()
            conexion.close()
            raise DBError("No existe el recurso solicitado")
        if producto[0] != id_usuario:
            cursor.close()
            conexion.close()
            raise DBError(f"No tienes permiso para actualizar este producto.")
        cursor.execute("DELETE FROM producto WHERE id_producto = %s AND id_usuario = %s", (id_producto, id_usuario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_productos_by_user(id_usuario)

    @classmethod
    def validarStockProducto(cls, id_producto, cantidad, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT stock FROM producto WHERE id_producto = %s AND id_usuario = %s", (id_producto, id_usuario))
        result = cursor.fetchone()
        cursor.close()
        conexion.close()
        if result:
            stock_disponible = result[0]
            if cantidad <= stock_disponible:
                return True  
            else:
                raise DBError(f"La cantidad solicitada supera el stock disponible para el producto {id_producto}.")
        else:
            raise DBError(f"Producto con id {id_producto} no encontrado")
        
    @classmethod
    def get_proveedores(cls, id_usuario, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            '''
            SELECT 
                proveedor.id_proveedor,
                proveedor.nombre AS nombre_proveedor
            FROM 
                producto
            INNER JOIN 
                producto_proveedor ON producto.id_producto = producto_proveedor.id_producto
            INNER JOIN 
                proveedor ON producto_proveedor.id_proveedor = proveedor.id_proveedor
            WHERE 
                producto.id_producto = %s AND producto.id_usuario = %s
            ''',
            (id_producto, id_usuario))
        proveedores = [
         {"id_proveedor": row[0], "nombre_proveedor": row[1]}
         for row in cursor.fetchall()]
        cursor.close()
        conexion.close()
        if not proveedores:
            raise DBError(f"No se encontraron proveedores para el producto {id_producto} y usuario {id_usuario}.")
        return proveedores
    

    @classmethod
    def updateStock(cls, id_usuario, id_producto, cantidad_decrementar):
        query = '''
        UPDATE producto 
        SET stock = stock - %s
        WHERE id_producto = %s AND id_usuario = %s
    '''
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(query, (cantidad_decrementar, id_producto, id_usuario))
        if cursor.rowcount == 0:
           raise DBError(f"No se encontró un producto con id {id_producto}")
        conexion.commit()
        cursor.close()
        conexion.close()
        return True


    @classmethod
    def get_productos_proveedores(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT 
            p.id_producto, p.nombre AS producto_nombre, p.descripcion,p.stock, pr.nombre AS proveedor_nombre
        FROM 
            producto p
        JOIN 
            producto_proveedor pp ON p.id_producto = pp.id_producto
        JOIN 
            proveedor pr ON pp.id_proveedor = pr.id_proveedor
        WHERE 
            p.id_usuario = %s;
    """, (id_usuario,))
        productos = [
        {
            "id_producto": row[0],
            "producto_nombre": row[1],
            "descripcion": row[2],
            "stock": row[3],
            "proveedor_nombre": row[4],
        }
        for row in cursor.fetchall()]
        cursor.close()
        conexion.close()
          
        #if not productos:
        #    raise DBError(f"No se encontraron productos")
        return productos

        

