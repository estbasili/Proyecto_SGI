# routes/user.py

from flask import Blueprint, request, jsonify
from models.usuario import Usuario

usuario_bp = Blueprint('usuario', __name__)


#################

# Get all users
@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.get_all()
    return jsonify(usuarios), 200

# Get user by ID
@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    usuario = Usuario.get_by_id(id_usuario)
    if usuario:
        return jsonify(usuario.a_json()), 200
    return jsonify({"error": "Usuario not found"}), 404

# Create a new user
@usuario_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    if not Usuario.validar_datos(data):
        return jsonify({"error": "Invalid data"}), 400
    Usuario.create(data)
    return jsonify({"message": "User created successfully"}), 201

# Update user
@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.json
    if not Usuario.validar_datos(data):
        return jsonify({"error": "Invalid data"}), 400
    Usuario.update(id_usuario, data)
    return jsonify({"message": "User updated successfully"}), 200

# Delete user
@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    Usuario.delete(id_usuario)
    return jsonify({"message": "User deleted successfully"}), 200