# models/usuario.py
from db.db import get_db_connection, DBError

class Usuario:
    schema = {
        "nombre": str,
        "email": str,
        "contraseña": str,
        "id_rol": int,
    }



    @classmethod
    def validar_datos(cls, data):
        if data is None or type(data) != dict:
            return False
        for key, key_type in cls.schema.items():
            if key not in data:
            # Si 'id_rol' no está presente en 'data', inicialízalo con 1
                if key == "id_rol":
                    data[key] = 1
                else:
                    return False
            elif type(data[key]) != key_type:
                return False
        return True

    def __init__(self, data):
        self.id_usuario = data[0]
        self.nombre = data[1]
        self.email = data[2]
        self.contraseña = data[3]
        # Inicializar id_rol a 1 si no está presente en data
        self.id_rol = data[4] if len(data) > 4 else 1


    def a_json(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "contarsena": self.contraseña,
            "id_rol": self.id_rol,
        }

    @classmethod
    def get_all(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, email, contraseña, id_rol FROM usuario")
        
        usuarios = []
        for usuario in cursor.fetchall():
            usuarios.append({
                "id_usuario": usuario[0],
                "nombre": usuario[1],
                "email":usuario[2],
                "contrasena":usuario[3],
                "id_rol":usuario [4],
            })

        cursor.close()
        conexion.close()
        
        return usuarios

    @classmethod
    def get_by_id(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre,email,contraseña,id_rol FROM usuario WHERE id_usuario = %s", (id_usuario,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        return cls(data) if data else None

    @classmethod
    def create(cls, data):
        if not cls.validar_datos(data):
            raise ValueError("Invalid data for Usuario")
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre,email,contraseña,id_rol) VALUES (%s,%s,%s,%s)",
            (data['nombre'],data['email'],data['contraseña'],data['id_rol'])
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def update(cls, id_usuario, data):
        if not cls.validar_datos(data):
            raise ValueError("Invalid data for Usuario")

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre = %s,email = %s,contraseña = %s,id_rol = %s, WHERE id_usuario = %s",
            (data['nombre'], data['email'], data['contraseña'], data['id_rol'], id_usuario)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @classmethod
    def delete(cls, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,)) ### saque una coma que detras de id_categoria
        conexion.commit()
        cursor.close()
        conexion.close()