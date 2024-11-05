# api/models/proveedor.py

from api.db.db import get_db_connection, DBError

class Proveedor:
    schema = {
        "nombre": str,
        "telefono": str,
        "email": str
    }

    @classmethod
    def validate(cls, data):
        """Valida que los datos contengan las claves requeridas y que los tipos de datos sean correctos."""
        if data is None or type(data) != dict:
            return False
        for key in cls.schema:
            if key not in data or type(data[key]) != cls.schema[key]:
                return False
        return True

    def __init__(self, data):
        """Inicializa un objeto Proveedor con datos del resultado de la consulta SQL."""
        self._id = data[0]
        self._nombre = data[1]
        self._telefono = data[2]
        self._email = data[3]

    def to_json(self):
        """Convierte el objeto Proveedor a formato JSON."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "telefono": self._telefono,
            "email": self._email,
        }

    @classmethod
    def get_proveedor_by_id(cls, id):
        """Obtiene un proveedor por su ID de la base de datos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id_proveedor = %s', (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if data:
            return Proveedor(data).to_json()
        
        raise DBError("No existe el proveedor solicitado")

    @classmethod
    def get_all_proveedores(cls):
        """Obtiene todos los proveedores de la base de datos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Proveedor(row).to_json() for row in data]

    @classmethod
    def add_proveedor(cls, data):
        """Agrega un nuevo proveedor a la base de datos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES (%s, %s, %s, %s)',
            (data["nombre"], data["telefono"], data["email"], data["id_usuario"])
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_proveedor(cls, id, data):
        """Actualiza un proveedor existente en la base de datos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE proveedor SET nombre = %s, telefono = %s, email = %s WHERE id_proveedor = %s',
            (data["nombre"], data["telefono"], data["email"], id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete_proveedor(cls, id):
        """Elimina un proveedor de la base de datos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM proveedor WHERE id_proveedor = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
