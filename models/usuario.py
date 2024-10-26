class Usuario:
    def __init__(self, id_usuario, nombre, password):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.password = password

    @staticmethod
    def obtener_por_nombre(nombre, db):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
        return cursor.fetchone()
