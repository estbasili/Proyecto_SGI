from api.db.db import get_db_connection, DBError
import logging

# Configuración de logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Estado:
    schema = {
        "id_estado": int,
        "descripcion": str
    }

    def __init__(self, data):
        if len(data) < 2:
            raise ValueError("Los datos deben contener al menos dos elementos: 'id_estado' y 'descripcion'.")
        self.id_estado = data[0]
        self.descripcion = data[1]

    def a_json(self):
        return {
            "id_estado": self.id_estado,
            "descripcion": self.descripcion,
        }

    @staticmethod
    def get_all_estados():
        conexion = get_db_connection()
        cursor = conexion.cursor()

        try:
            cursor.execute('SELECT * FROM estados_orden_compra')
            data = cursor.fetchall()

            if not data:
                raise DBError('No existe el recurso solicitado.')

            # Convertir las filas recuperadas a objetos Estado y luego a JSON
            estados = [Estado(fila).a_json() for fila in data]
            return estados

        except Exception as e:
            logging.error(f"Error al recuperar los estados: {str(e)}")
            raise DBError('Error al recuperar los estados desde la base de datos.')
        
        finally:
            cursor.close()
            conexion.close()

