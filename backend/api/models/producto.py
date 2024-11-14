from db.db import get_db_connection, DBError

class Producto:
    schema = {
        "nombre": str,
        "descripcion": str,
        "precio": float,
        "stock": int,
        "id_categoria": int,
        "id_usuario": int,
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
            "id_usuario": self.id_usuario,
        }

    @classmethod
    def get_all(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        # Ejecutar la consulta con JOIN para obtener el nombre de la categoría
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
        """)

        # Transformamos los resultados a formato JSON
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

        return productos

    @classmethod
    def get_by_id(cls, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        return cls(data) if data else None

    @classmethod
    def create(cls, data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO producto (nombre, descripcion, precio, stock, id_categoria, id_usuario) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['nombre'], data['descripcion'], data['precio'], data['stock'], data['id_categoria'], data['id_usuario'])
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def update(cls, id_producto, data):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s, id_usuario = %s WHERE id_producto = %s", #############################
            (data['nombre'], data['descripcion'], data['precio'], data['stock'], data['id_categoria'], data['id_usuario'], id_producto)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def delete(cls, id_producto):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id_producto,))##########################################correccion de id_producto
        conexion.commit()
        cursor.close()
        conexion.close()
