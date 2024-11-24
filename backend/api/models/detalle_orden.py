from api.db.db import get_db_connection, DBError
from api.models.producto import Producto

class DetalleOrden:
    schema = {
        "id_orden": int,
        "id_producto": int, 
        "cantidad": str,
    }
    @classmethod
    
    def a_json(self):
        return {
            "id_orden": self.id_orden,
            "id_producto": self.id_producto if self.id_producto else None,
            "cantidad": self.cantidad if self.cantidad else None,
        }

    def __init__(self, data):
        self.id_detalle = data[0]  # Asume que este es un entero o similar
        self.id_orden = data[1]  # Asume que este es un entero
        self.id_producto = data[2]  # Asume que este es un entero o cadena
        self.cantidad = data[3]  # Asume que este es un entero


    @classmethod
    def validar_datos(cls, data):
        # Validar que data sea una lista
        print("Validando los datos recibidos...")
        if not isinstance(data, list):
            return False, "Error: Los datos no son una lista."

        # Variable para almacenar los productos sin stock
        productos_sin_stock = []

        # Recorrer cada elemento en la lista
        for i, renglon in enumerate(data):
            try:
                print(f"Validando renglón {i + 1}...")

                # Verificar si las claves 'id_producto' y 'cantidad' existen en el renglon
                if 'id_producto' not in renglon or 'cantidad' not in renglon:
                    return False, f"Error en el renglón {i + 1}: Faltan claves 'id_producto' o 'cantidad'."

                id_producto = renglon['id_producto']
                cantidad = renglon['cantidad']

                # Validar que id_producto y cantidad sean del tipo esperado
                if not isinstance(id_producto, str):
                    return False, f"Error en el renglón {i + 1}: 'id_producto' debe ser una cadena."
                if not isinstance(cantidad, int):
                    return False, f"Error en el renglón {i + 1}: 'cantidad' debe ser un número entero."

                # Validar que la cantidad sea un valor positivo
                if cantidad <= 0:
                    return False, f"Error en el renglón {i + 1}: 'cantidad' debe ser un número positivo."

                print(f"Renglón {i + 1}: id_producto = {id_producto}, cantidad = {cantidad}")

                # Verificar si el producto tiene stock disponible
                print(f"Verificando stock para el producto {id_producto} con cantidad {cantidad}...")
                if not Producto.validarStockProducto(id_producto, cantidad):
                    print(f"Producto {id_producto} sin stock.")
                    productos_sin_stock.append(id_producto)  # Guardar el id del producto sin stock

            except KeyError as e:
                # Capturar error si falta alguna clave en el renglón
                return False, f"Error en el renglón {i + 1}: Falta la clave '{e.args[0]}'."
            except TypeError as e:
                # Capturar error de tipo si el renglón no tiene la estructura correcta
                return False, f"Error en el renglón {i + 1}: Estructura del renglón inválida."
            except Exception as e:
                # Capturar cualquier otro tipo de error inesperado
                return False, f"Error en el renglón {i + 1}: {str(e)}"

        # Si hay productos sin stock, devolver mensaje con todos los productos sin stock
        if productos_sin_stock:
            productos_sin_stock_str = ", ".join(productos_sin_stock)
            print(f"Productos sin stock: {productos_sin_stock_str}")
            return False, f"Productos sin stock: {productos_sin_stock_str}"

        print("Todos los renglones son válidos. Validación exitosa.")
        # Si todos los renglones son válidos
        return True, "Validación exitosa. Todos los renglones son válidos."

    @classmethod
    def createDetalleOrden(cls, id_orden, productos):
        # Imprime el ID de la orden recibida
        print(f"ID de la orden recibida: {id_orden}")
        
        # Imprime los productos recibidos
        print("Productos recibidos:")
        for i, producto in enumerate(productos, start=1):
            print(f"  Producto {i}: {producto}")

        # Validar que los productos tienen los campos requeridos
        for producto in productos:
            if not all(key in producto for key in ['id_producto', 'cantidad']):
                raise ValueError(f"El producto {producto} no contiene todos los campos requeridos: 'id_producto' y 'cantidad'.")

        # Preparar conexión y cursor para la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            # Preparar la consulta para insertar
            query = '''
                INSERT INTO detalle_orden (id_orden, id_producto, cantidad)
                VALUES (%s, %s, %s)
            '''
            
            # Insertar cada producto en la tabla detalle_orden
            for producto in productos:
                valores = (id_orden, producto['id_producto'], producto['cantidad'])
                Producto.updateStock(producto['id_producto'],producto['cantidad'])
                print(f"Ejecutando query: {query} con valores {valores}")
                cursor.execute(query, valores)

            # Confirmar los cambios en la base de datos
            conexion.commit()
            print("Todos los productos se insertaron correctamente.")
            return True
        except Exception as e:
            # Revertir la transacción en caso de error
            conexion.rollback()
            print(f"Error al insertar los productos en detalle_orden: {str(e)}")
            raise
        finally:
            # Cerrar cursor y conexión
            cursor.close()
            conexion.close()

