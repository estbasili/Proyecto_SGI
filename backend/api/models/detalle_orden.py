from api.db.db import get_db_connection, DBError
from api.models.producto import Producto


class DetalleOrden:
    schema = {
        "id_orden": int,
        "id_producto": int, 
        "cantidad": str,
    }
    
    @classmethod
    def a_json(cls, id_usuario):
        # Aquí puedes personalizar cómo retornar los detalles con id_usuario si es necesario
        return {
            "id_orden": cls.id_orden,
            "id_producto": cls.id_producto if cls.id_producto else None,
            "cantidad": cls.cantidad if cls.cantidad else None,
        }

    def __init__(self, data):
        self.id_detalle = data[0]  # Asume que este es un entero o similar
        self.id_orden = data[1]  # Asume que este es un entero
        self.id_producto = data[2]  # Asume que este es un entero o cadena
        self.cantidad = data[3]  # Asume que este es un entero

    @classmethod
    def validar_datos(cls, data, id_usuario):
        if not isinstance(data, list):
            return False, "Error: Los datos no son una lista."

        # Variable para almacenar los productos sin stock
        productos_sin_stock = []

        # Recorrer cada elemento en la lista
        for i, renglon in enumerate(data):
            try:
                # Verificar si las claves 'id_producto' y 'cantidad' existen en el renglón
                if not isinstance(renglon, dict):
                    return False, f"Error en el renglón {i + 1}: No es un diccionario."

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

                if not Producto.validarStockProducto(id_producto, cantidad, id_usuario):
                    productos_sin_stock.append(id_producto)  # Guardar el id del producto sin stock

            except Exception as e:
                # Capturar cualquier otro tipo de error inesperado
                return False, f"Error en el renglón {i + 1}: {str(e)}"

        # Si hay productos sin stock, devolver mensaje con todos los productos sin stock
        if productos_sin_stock:
            productos_sin_stock_str = ", ".join(productos_sin_stock)
            return False, f"Productos sin stock: {productos_sin_stock_str}"

        # Si todos los renglones son válidos
        return True, "Validación exitosa. Todos los renglones son válidos."


    @classmethod
    def createDetalleOrden(cls, id_orden, productos, id_usuario):        
        # Imprime los productos recibidos        
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
                # Extraer id_producto y cantidad correctamente
                id_producto = producto.get('id_producto')
                cantidad = producto.get('cantidad')

                # Asegurarse de que los valores sean válidos
                if not isinstance(id_producto, str):
                    raise ValueError(f"El 'id_producto' debe ser una cadena, pero se recibió: {id_producto}")
                if not isinstance(cantidad, int) or cantidad <= 0:
                    raise ValueError(f"La 'cantidad' debe ser un número entero positivo, pero se recibió: {cantidad}")

                # Preparar valores para la consulta
                valores = (id_orden, id_producto, cantidad)

                # Actualizar el stock del producto
                Producto.updateStock(id_usuario, id_producto, cantidad)

                # Ejecutar la consulta
                cursor.execute(query, valores)

            # Confirmar los cambios en la base de datos
            conexion.commit()
            return True
        except Exception as e:
            # Revertir la transacción en caso de error
            conexion.rollback()
            raise
        finally:
            # Cerrar cursor y conexión
            cursor.close()
            conexion.close()

