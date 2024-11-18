from db.db import DBError
from flask import Blueprint, request, jsonify
from models.usuario import Usuario



usuario_bp = Blueprint('usuario', __name__)

# Obtener todos los usuarios
@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.get_all()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Obtener usuario por ID
@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    try:
        usuario = Usuario.get_by_id(id_usuario)
        return jsonify(usuario), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    


# Crea un usuario metodo Carlos
@usuario_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        usuario = Usuario.register(data)
        print (usuario)
        return jsonify( usuario ), 201
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify( {"message": e.args[0]} ), 400
    

# agregacion de loggin
@usuario_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    try:
        usuario = Usuario.login(auth)
        return jsonify( usuario ), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify( {"message": e.args[0]} ), 400




# Crear un nuevo usuario--------------No puedo hacer que ande cuando id_rol es una cadena vacia
#@usuario_bp.route('/usuarios', methods=['POST'])
#def create_usuario():
    try:
        data = request.json
        response = Usuario.create(data)
        return jsonify(response), 201
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500


# Actualizar un usuario
#@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
#def update_usuario(id_usuario):
    try:
        data = request.json
        response = Usuario.update(id_usuario, data)  
        return jsonify(response), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500


# Eliminar un usuario
#@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
#def delete_usuario(id_usuario):
    try:
        response = Usuario.delete(id_usuario)
        return jsonify(response), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400
