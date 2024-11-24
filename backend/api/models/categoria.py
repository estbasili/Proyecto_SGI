from api.db.db import get_db_connection, DBError

class Categoria:
    schema = {
        "nombre": str
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
        self.id_categoria = data[0]
        self.nombre = data[1]

    def a_json(self):
        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre
        }

    @classmethod
    def get_all_by_user(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria WHERE id_usuario = %s", (id_usuario,))
        categorias = cursor.fetchall()
        if not categorias:
            raise DBError("No existe el recurso solicitado")
        categorias_json = [cls(categoria).a_json() for categoria in categorias]
        cursor.close()
        conexion.close()
        return categorias_json


    @classmethod
    def get_by_id_categoria(cls, id_usuario, id_categoria):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
        "SELECT id_categoria, nombre FROM categoria WHERE id_categoria = %s AND id_usuario = %s",
        (id_categoria, id_usuario) )
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if not data:
            raise DBError("No existe el recurso solicitado")
        return cls(data)


    @classmethod
    def create_by_user(cls, data, id_usuario):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM categoria WHERE id_usuario = %s AND nombre = %s", (id_usuario, data['nombre']))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            raise DBError("La categoría ya existe")
        cursor.execute(
        "INSERT INTO categoria (nombre, id_usuario) VALUES (%s, %s)",
        (data['nombre'], id_usuario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_all_by_user(id_usuario)


    @classmethod
    def update_by_user(cls, data, id_usuario,id_categoria):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM categoria WHERE id_usuario = %s AND nombre = %s AND id_categoria != %s", 
                       (id_usuario, data['nombre'], id_categoria))
        if cursor.fetchone():
            raise DBError("La categoría con ese nombre ya existe")
        cursor.execute(
            "UPDATE categoria SET nombre = %s WHERE id_categoria = %s AND id_usuario = %s",
            (data['nombre'], id_categoria, id_usuario))
        if cursor.rowcount == 0:
            raise DBError("No existe el recurso soliictado")
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_all_by_user(id_usuario)


    @classmethod
    def delete_by_user(cls, id_usuario, id_categoria):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM categoria WHERE id_categoria = %s AND id_usuario = %s",
            (id_categoria, id_usuario))
        if cursor.rowcount == 0:
            raise DBError("No existe el recurso solicitado")
        conexion.commit()
        cursor.close()
        conexion.close()
        return cls.get_all_by_user(id_usuario)
