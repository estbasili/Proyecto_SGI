from api import app
from api.db.db import DBError
from flask import request, jsonify
from api.models.usuario import Usuario
from base64 import b64decode

# Obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.get_all()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Obtener usuario por ID
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    try:
        usuario = Usuario.get_by_id(id_usuario)
        return jsonify(usuario), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    


# Crea un usuario metodo Carlos
@app.route('/register', methods=['POST'])
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

"""@app.route('/login', methods=['POST'])
def login():
    print("Encabezados recibidos:", request.headers)

    auth_header = request.headers.get('Authorization')  # Obtén el encabezado Authorization
    if auth_header and auth_header.startswith('Basic '):
        try:
            # Decodifica el contenido del encabezado Authorization
            auth_decoded = b64decode(auth_header.split(' ')[1]).decode('utf-8')
            email, password = auth_decoded.split(':')
            #print(f"Email recibido: {email}, Contraseña recibida: {password}")
        except Exception as e:
            return jsonify({"message": "Error al procesar las credenciales"}), 400
    else:
        return jsonify({"message": "No autorizado"}), 401

    try:
        # Llama al método login de Usuario con los datos decodificados
        usuario = Usuario.login({"email": email, "password": password})
        return jsonify(usuario), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": str(e)}), 400"""




@app.route('/login', methods=['POST'])
def login():
    try:
        # Asegurarte de que la solicitud contiene un cuerpo JSON
        if not request.is_json:
            return jsonify({"message": "El cuerpo de la solicitud debe ser JSON"}), 400
        
        # Obtén los datos de autenticación desde la solicitud
        auth = request.get_json()
        
        # Usa el método login de Usuario para validar las credenciales y generar el token
        login_result = Usuario.login(auth)
        
        # Retorna el resultado del login
        return jsonify(login_result), 200
    except DBError as db_err:
        # Manejo específico de errores personalizados
        return jsonify({"message": db_err.args[0]["message"]}), db_err.args[0]["code"]
    except Exception as e:
        # Captura errores generales
        return jsonify({"message": f"Error del servidor: {str(e)}"}), 500

    