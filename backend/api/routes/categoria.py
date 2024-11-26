from api import app
from api.db.db import DBError
from flask import request, jsonify
from api.models.categoria import Categoria
from api.utils.security import token_required  # Decorador de autenticación

@app.route('/usuarios/<int:id_usuario>/categorias', methods=['GET'])
@token_required
def get_categorias_by_user(id_usuario):
    try:
        categorias = Categoria.get_all_by_user(id_usuario)
        return jsonify(categorias), 200 
    except DBError as e:
        return jsonify({"message": str(e)}), 203
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500

@app.route('/usuarios/<int:id_usuario>/categorias/<int:id_categoria>', methods=['GET'])
@token_required
def get_categoria(id_usuario, id_categoria):
    try:
        categoria = Categoria.get_by_id_categoria(id_usuario, id_categoria)
        return jsonify(categoria.a_json()), 200  
    except DBError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500

@app.route('/usuarios/<int:id_usuario>/categorias', methods=['POST'])
@token_required
def create_categoria(id_usuario):
    data = request.get_json()
    try:
        Categoria.create_by_user(data, id_usuario)
        categorias = Categoria.get_all_by_user(id_usuario) 
        return jsonify(categorias), 201  
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500

@app.route('/usuarios/<int:id_usuario>/categorias/<int:id_categoria>', methods=['PUT'])
@token_required
def update_categoria(id_usuario, id_categoria):
    data = request.get_json()
    try:
        Categoria.update_by_user(data, id_usuario, id_categoria)
        categorias = Categoria.get_all_by_user(id_usuario) 
        return jsonify(categorias), 200  
    except DBError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500

@app.route('/usuarios/<int:id_usuario>/categorias/<int:id_categoria>', methods=['DELETE'])
@token_required
def delete_categoria(id_usuario, id_categoria):
    try:
        Categoria.delete_by_user(id_usuario, id_categoria)
        categorias = Categoria.get_all_by_user(id_usuario)  
        return jsonify(categorias), 200  
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Error inesperado: " + str(e)}), 500
