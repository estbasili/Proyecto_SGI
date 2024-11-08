from db.db import get_db_connection, DBError

class Proveedor:
    schema = {
        "nombre": str,
        "telefono": str,
        "email": str,
        "id_usuario": int,
    }

    @classmethod
    def validar_datos(cls,data):
        if data == None or type(data) != dict:
            return False
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto?
            if type(data[key]) != cls.schema[key]: 
                return False
        return True

    def __init__(self, data):
        self.id_proveedor = data[0]
        self.nombre = data[1]
        self.telefono = data[2]
        self.email = data[3]
        self.id_usuario = data[4]

    def a_json(self):
        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "id_usuario": self.id_usuario
        }

    
    @classmethod
    def get_all_proveedores(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM proveedor')
        data = cursor.fetchall()
        cursor.close()
        conexion.close()

        proveedores = [Proveedor(proveedor).a_json() for proveedor in data]
        return proveedores

    