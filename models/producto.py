import mysql.connector  # Asegúrate de importar mysql.connector

from db.db_config import get_db_connection

class Producto:
    # Definición del esquema como antes
    schemas = {
        "nombre": str,
        "descripcion": str,
        "precio": str,
        "stock": int,
        "id_categoria": int,
        "id_usuario": int
    }

    def __init__(self, data):
        self.id = data[0]
        self.nombre = data[1]
        self.descripcion = data[2]
        self.precio = data[3]
        self.stock = data[4]
        self.id_categoria = data[5]
        self.id_usuario = data[6]
    
    @staticmethod
    def get_all_tabla():
        try:
            with get_db_connection() as connection:  # Usar contexto para manejar la conexión
                print("Conectando a la base de datos...")  # Traza de conexión
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM producto")
                results = cursor.fetchall()

                print("Consulta ejecutada correctamente.")  # Traza después de ejecutar la consulta
                print(f"Resultados obtenidos: {results}")  # Muestra los resultados obtenidos

                return [Producto(row) for row in results] if results else []  # Retorna lista vacía si no hay resultados
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos o al ejecutar la consulta: {err}")
            return None  # Retorna None si hay un error
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None  # Retorna None si hay un error inesperado

    @staticmethod
    def get_all():
        # Datos ficticios de ejemplo
        fake_data = [
            (1, "Producto 1", "Descripción del Producto 1", "10.00", 100, 1, 1),
            (2, "Producto 2", "Descripción del Producto 2", "20.00", 50, 1, 2),
            (3, "Producto 3", "Descripción del Producto 3", "30.00", 0, 2, 1),
            (4, "Producto 4", "Descripción del Producto 4", "40.00", 25, 2, 2)
        ]

        # Retornar una lista de instancias de Producto
        return [Producto(row) for row in fake_data]
