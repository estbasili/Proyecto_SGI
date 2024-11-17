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
            elif key == "id_rol" and (data[key] == "" or type(data[key]) != key_type):  # Acepta "" y verifica tipo para id_rol
            # Si es una cadena vacía, asigna el valor por defecto
                data[key] = 1
            elif type(data[key]) != key_type:
                return False
        return True


    def __init__(self, data):
        self.id_usuario = data[0]
        self.nombre = data[1]
        self.email = data[2]
        self.contraseña = data[3]
        self.id_rol = data[4] if len(data) > 4 else 1  # Asignar id_rol a 1 si no está presente

    def a_json(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "contraseña": self.contraseña,
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
                "email": usuario[2],
                "contraseña": usuario[3],
                "id_rol": usuario[4],
            })

        cursor.close()
        conexion.close()
        return usuarios

    @classmethod
    def get_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if data:
            return Usuario(data).a_json()
        raise DBError('No existe el recurso solicitado')

    @classmethod
    def create(cls, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Control si el email no esta en uso por otro usuario
        email = data["email"]
        cursor.execute('SELECT * FROM usuario WHERE email = %s', (email,))
        row = cursor.fetchone()
        if row is not None:
            raise DBError("Email ya registrado")
        
        cursor.execute(
            "INSERT INTO usuario (nombre, email, contraseña, id_rol) VALUES (%s, %s, %s, %s)",
            (data['nombre'], data['email'], data['contraseña'], data['id_rol'])
        )
        conexion.commit()
        id_usuario = cursor.lastrowid
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario creado exitosamente", "id_usuario": id_usuario}

    @classmethod
    def update(cls, id, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute(
            "UPDATE usuario SET nombre = %s, email = %s, contraseña = %s, id_rol = %s WHERE id_usuario = %s",
            (data['nombre'], data['email'], data['contraseña'], data['id_rol'], id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario actualizado"}

    @classmethod
    def delete(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute('DELETE FROM usuario WHERE id_usuario = %s', (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario eliminado"}
