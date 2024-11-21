from api import app
from flask import request, jsonify
from api.models.categoria import Categoria

# Get all categories
@app.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.get_all()
    return jsonify(categorias), 200

# Get category by ID
@app.route('/categorias/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    categoria = Categoria.get_by_id(id_categoria)
    if categoria:
        return jsonify(categoria.a_json()), 200
    return jsonify({"error": "Category not found"}), 404

# Create a new category
@app.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.json
    if not Categoria.validar_datos(data):
        return jsonify({"error": "Invalid data"}), 400
    Categoria.create(data)
    return jsonify({"message": "Category created successfully"}), 201

# Update category
@app.route('/categorias/<int:id_categoria>', methods=['PUT'])
def update_categoria(id_categoria):
    data = request.json
    if not Categoria.validar_datos(data):
        return jsonify({"error": "Invalid data"}), 400
    Categoria.update(id_categoria, data)
    return jsonify({"message": "Category updated successfully"}), 200

# Delete category
@app.route('/categorias/<int:id_categoria>', methods=['DELETE'])
def delete_categoria(id_categoria):
    Categoria.delete(id_categoria)
    return jsonify({"message": "Category deleted successfully"}), 200
