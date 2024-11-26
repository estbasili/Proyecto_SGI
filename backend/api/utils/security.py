from flask import request, jsonify
import jwt
from functools import wraps
from api import app
from api.db.db import get_db_connection, DBError


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(kwargs)
        token = None


        # La solicitud en una ruta protegida debe incluir una cabecera 'x-access-token' con 
        # el valor del token obtenido en el login
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({"message": "Falta el token"}), 401
        
        # Para acceder a recursos de un usuario específico, la ruta debe incluir el id_user
        # Para acceder a recursos comunes a cualquier usuario, la solicitud debe contener
        # una cabecera personalizada id_user, con el valor correspondiente
        id_usuario = None


        # Primero se verifica si la ruta tiene el id_user
        print("Argumentos de la solicitud: ", kwargs)
        if 'id_usuario' in kwargs:
            id_usuario = kwargs['id_usuario']


        if id_usuario is None:
            # Si no está en la ruta, debe estar en la cabecera
            if 'id-usuario' in request.headers:
                usuario_id = request.headers['id-usuario']



        # Si no se envió el id_user en ninguno de los dos formatos, se bloquea el acceso al recurso
        # y se rechaza la solicitud
        if id_usuario is None:
            return jsonify({"message": "Falta el usuario"}), 401
        
        # El id_user debe coincidir con el propietario del token
        # Se decodifica y se comprueba si son iguales
        try:
            data = jwt.decode(token , app.config['SECRET_KEY'], algorithms = ['HS256'])
            token_id = data['id_usuario']
            # Imprime el token decodificado para ver su contenido
            print("Token decodificado:", data)

            if int(id_usuario) != int(token_id):
                return jsonify({"message": "Error de id"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}), 401


        # Si no hubo un retorno previo, entonces el token es válido y pertenece 
        # al usuario que realiza la solicitud, se continua la ejecución de la consulta
        return func(*args, **kwargs)
    return decorated