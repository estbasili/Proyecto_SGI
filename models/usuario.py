class Usuario:
    def __init__(self, id_usuario, nombre, email, password):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email, db):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        return cursor.fetchone()
