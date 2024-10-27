from flask_login import UserMixin
from db.db_config import get_db_connection

class User(UserMixin):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre FROM usuarios WHERE id_usuario = %s", (user_id,))####### modificar aca mañana
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return User(row[0], row[1])
        return None