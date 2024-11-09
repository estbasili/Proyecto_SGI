# models/categoria.py
from db.db import get_db_connection, DBError

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
            "nombre": self.nombre,
        }

    @classmethod
    def get_all(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria")
        
        categorias = []
        for categoria in cursor.fetchall():
            categorias.append({
                "id_categoria": categoria[0],
                "nombre": categoria[1]
            })

        cursor.close()
        conexion.close()
        
        return categorias

    @classmethod
    def get_by_id(cls, id_categoria):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria WHERE id_categoria = %s", (id_categoria,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        return cls(data) if data else None

    @classmethod
    def create(cls, data):
        if not cls.validar_datos(data):
            raise ValueError("Invalid data for Categoria")
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO categoria (nombre) VALUES (%s)",
            (data['nombre'],)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def update(cls, id_categoria, data):
        if not cls.validar_datos(data):
            raise ValueError("Invalid data for Categoria")

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE categoria SET nombre = %s WHERE id_categoria = %s",
            (data['nombre'], id_categoria)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def delete(cls, id_categoria):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", (id_categoria,))
        conexion.commit()
        cursor.close()
        conexion.close()
