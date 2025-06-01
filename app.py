# --------------------
# IMPORTACIONES
# --------------------
from flask import Flask, jsonify, request, render_template, url_for, redirect, session
from datetime import datetime
import os
import requests
import re
from functools import wraps
from werkzeug.utils import secure_filename

from models.conexion import ConexionMySQL
from models.videojuego import VideogamesMySQL
from models.categoria import CategoriesMySQL
from models.genero import GendersMySQL
from models.plataforma import PlatfomsMySQL
from models.producto import ProductsMySQL
from models.login import LoginMySQL

# --------------------
# CONFIGURACIÓN
# --------------------
app = Flask(__name__)
app.secret_key = "tu_secreto"

# --------------------
# FUNCIONES AUXILIARES
# --------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'AdminUserName' not in session:
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function

# --------------------
# AUTENTICACIÓN
# --------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'AdminUserName' not in data or 'AdminContraseña' not in data:
        return jsonify({"status": "error", "message": "Faltan datos"}), 400

    login = LoginMySQL.GetAdmin(data)
    if login:
        session['AdminUserName'] = data['AdminUserName']
        return jsonify({"status": "success", "message": "Inicio de sesión exitoso", "redirect": url_for('principal')})
    else:
        return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

# --------------------
# CATEGORÍAS
# --------------------
@app.route('/category', methods=['GET'])
def get_all_categories():
    categories = CategoriesMySQL.ViewCategories()
    return jsonify(categories), 200

@app.route('/category/<int:id>', methods=['GET'])
def get_all_categories_by_id(id):
    categories = CategoriesMySQL.ViewCategoriesByID(id)
    if categories:
        return jsonify(categories), 200
    else:
        return jsonify({'message': 'Categoria no encontrada'}), 404

@app.route('/category/<int:id>', methods=['PUT'])
def update_categories(id):
    data = request.json
    CategoriesMySQL.UpdateCategories(data, id)
    return jsonify({'message': 'Categoria actualizada'}), 200

@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    id = CategoriesMySQL.CreateCategory(data)
    return jsonify({'message': 'Categoria creada', 'CategoriaID': id}), 201

@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id):
    CategoriesMySQL.DeleteCategory(id)
    return jsonify({'message': 'Categoria eliminada'}), 200

# --------------------
# GÉNEROS
# --------------------
@app.route('/gender', methods=['GET'])
def get_all_gender():
    gender = GendersMySQL.ViewGenders()
    return jsonify(gender), 200

@app.route('/gender/<int:id>', methods=['GET'])
def get_all_gender_by_id(id):
    gender = GendersMySQL.ViewGendersByID(id)
    if gender:
        return jsonify(gender), 200
    else:
        return jsonify({'message': 'Genero no encontrado'}), 404
    
@app.route('/gender/<int:id>', methods=['PUT'])
def update_genders(id):
    data = request.json
    GendersMySQL.UpdateGenders(data, id)
    return jsonify({'message': 'Genero actualizado'}), 200
    
@app.route('/gender', methods=['POST'])
def create_gender():
    data = request.json
    id = GendersMySQL.CreateGenders(data)
    return jsonify({'message': 'Genero creada', 'GeneroID': id}), 201

@app.route('/gender/<int:id>', methods=['DELETE'])
def delete_gender(id):
    GendersMySQL.DeleteGenders(id)
    return jsonify({'message': 'Genero eliminado'}), 200

# --------------------
# PLATAFORMAS
# --------------------
@app.route('/platform', methods=['GET'])
def get_all_platform():
    platform = PlatfomsMySQL.ViewPlatfoms()
    return jsonify(platform), 200

@app.route('/platform/<int:id>', methods=['GET'])
def get_all_platform_by_id(id):
    platform = PlatfomsMySQL.ViewPlatfomsByID(id)
    if platform:
        return jsonify(platform), 200
    else:
        return jsonify({'message': 'Plataforma no encontrada'}), 404
    
@app.route('/platform/<int:id>', methods=['PUT'])
def update_platforms(id):
    data = request.json
    PlatfomsMySQL.UpdatePlatfoms(data, id)
    return jsonify({'message': 'Plataforma actualizada'}), 200
    
@app.route('/platform', methods=['POST'])
def create_platform():
    data = request.json
    id = PlatfomsMySQL.CreatePlatforms(data)
    return jsonify({'message': 'Plataforma creada', 'PlataformaID': id}), 201

@app.route('/platform/<int:id>', methods=['DELETE'])
def delete_platform(id):
    PlatfomsMySQL.DeletePlatforms(id)
    return jsonify({'message': 'Plataforma eliminada'}), 200

# --------------------
# PRODUCTOS
# --------------------
@app.route('/product', methods=['GET'])
def get_all_product():
    product = ProductsMySQL.ViewProducts()
    return jsonify(product), 200

@app.route('/product/<int:id>', methods=['GET'])
def get_all_product_by_id(id):
    product = ProductsMySQL.ViewProductsByID(id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    nombre = request.form.get('ProductoNombre')
    descripcion = request.form.get('ProductoDescripcion')
    categoria_id = request.form.get('CategoriaID')
    precio = request.form.get('ProductoPrecio')
    stock = request.form.get('ProductoStock')
    
    imagen = request.files.get('ProductoFoto')

    if imagen:
        # Crear nombre de archivo consistente
        nombre_procesado = nombre.lower().replace(' ', '_').strip()
        filename = f"{nombre_procesado}.jpg"
        imagen.save(f'./static/img/productos/{filename}')

    # Agrega filename si quieres actualizar la imagen también en la DB
    ProductsMySQL.UpdateProducts(nombre, descripcion, categoria_id, precio, stock, id)

    return jsonify({'message': 'Producto actualizado'}), 200

@app.route('/product', methods=['POST'])
def create_product():
    nombre = request.form.get('ProductoNombre')
    descripcion = request.form.get('ProductoDescripcion')
    categoria_id = request.form.get('CategoriaID')
    precio = request.form.get('ProductoPrecio')
    stock = request.form.get('ProductoStock')

    imagen = request.files.get('ProductoFoto')
    
    if imagen:
        # Crear nombre de archivo consistente
        nombre_procesado = nombre.lower().replace(' ', '_').strip()
        filename = f"{nombre_procesado}.jpg"
        imagen.save(f'./static/img/productos/{filename}')

    id = ProductsMySQL.CreateProducts(nombre, descripcion, categoria_id, precio, stock)
    
    return jsonify({'message': 'Producto agregado', 'ProductoID': id}), 201

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    ProductsMySQL.DeleteProduct(id)
    return jsonify({'message': 'Producto eliminado'}), 200

# --------------------
# VIDEOJUEGOS
# --------------------
@app.route('/games', methods=['GET'])
def get_all_games():
    games = VideogamesMySQL.ViewGames()
    return jsonify(games), 200

@app.route('/gamescard', methods=['GET'])
def get_three_games():
    games = VideogamesMySQL.ViewGameCard()
    return jsonify(games), 200

@app.route('/games/<int:id>', methods=['GET'])
def get_game_by_id(id):
    game = VideogamesMySQL.ViewGamesByID(id)
    if game:
        return jsonify(game), 200
    else:
        return jsonify({'message': 'Videojuego no encontrado'}), 404
    
@app.route('/games/<int:id>', methods=['PUT'])
def update_games(id):
    nombre = request.form.get('VideojuegoNombre')
    descripcion = request.form.get('VideojuegoDescripcion')
    plataforma_id = request.form.get('PlataformaID')  # revisar mayúsculas/minúsculas exactas
    genero_id = request.form.get('GeneroID')
    precio = request.form.get('VideojuegoPrecio')
    lanzamiento = request.form.get('VideojuegoLanzamiento')
    stock = request.form.get('VideojuegoStock')
    
    imagen = request.files.get('VideojuegoFoto')

    if imagen:
        # Crear nombre de archivo consistente
        nombre_procesado = nombre.lower().replace(' ', '_').strip()
        filename = f"{nombre_procesado}.jpg"
        imagen.save(f'./static/img/juegos/{filename}')

    # Aquí agrega la lógica para actualizar la base de datos
    VideogamesMySQL.UpdateGame(nombre, descripcion, plataforma_id, genero_id, precio, lanzamiento, stock, id)

    return jsonify({'message': 'Videojuego actualizado'}), 200

@app.route('/games', methods=['POST'])
def create_games():
    nombre = request.form.get('VideojuegoNombre')
    descripcion = request.form.get('VideojuegoDescripcion')
    plataforma_id = request.form.get('PlataformaID')  # revisar mayúsculas/minúsculas exactas
    genero_id = request.form.get('GeneroID')
    precio = request.form.get('VideojuegoPrecio')
    lanzamiento = request.form.get('VideojuegoLanzamiento')
    stock = request.form.get('VideojuegoStock')
    
    imagen = request.files.get('VideojuegoFoto')

    if imagen:
        # Crear nombre de archivo consistente
        nombre_procesado = nombre.lower().replace(' ', '_').strip()
        filename = f"{nombre_procesado}.jpg"
        imagen.save(f'./static/img/juegos/{filename}')

    # Aquí agrega la lógica para actualizar la base de datos
    id = VideogamesMySQL.CreateGames(nombre, descripcion, plataforma_id, genero_id, precio, lanzamiento, stock)

    return jsonify({'message': 'Videojuego creado', 'VideojuegoID': id}), 201


@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    success = VideogamesMySQL.DeleteGame(id)
    if success:
        return jsonify({'message': 'Videojuego eliminado'}), 200
    return jsonify({'message': 'Videojuego no encontrado'}), 404

# --------------------
# RUTAS DE TEMPLATES
# --------------------
@app.route('/')
def home():
    return render_template('inicio.html', title="Inicio")

@app.route('/videojuegos')
def videojuegos():
    return render_template('videojuegos.html', title="Videojuegos")

@app.route('/productos')
def productos():
    return render_template('productos.html', title="Productos")

@app.route('/ver_juego/<int:id>')
def ver_juego(id):
    juego = VideogamesMySQL.ViewGamesByID(id)
    if not juego:
        return "Juego no encontrado", 404
    return render_template('detalles.html', juego=juego)

@app.route('/ver_producto/<int:id>')
def ver_producto(id):
    producto = ProductsMySQL.ViewProductsByID(id)
    if not producto:
        return "Producto no encontrado", 404
    return render_template('detalle.html', producto=producto)

@app.route('/admin')
def admin():
    return render_template('sesion.html', title='Inicio de Sesión')

@app.route('/principal')
@login_required
def principal():
    return render_template('inicio_admin.html', title="Principal")

@app.route('/categoria_admin')
@login_required
def categoria():
    return render_template('catergoria_admin.html', title="Categoria")

@app.route('/genero_admin')
@login_required
def genero():
    return render_template('genero_admin.html', title="Genero")

@app.route('/plataforma_admin')
@login_required
def plataforma():
    return render_template('plataforma_admin.html', title="Plataforma")

@app.route('/producto_admin')
@login_required
def producto():
    return render_template('producto_admin.html', title="Producto")

@app.route('/videojuego_admin')
@login_required
def videojuego():
    return render_template('/videojuegos_admin.html', title='Videojuego')

# --------------------
# EJECUCIÓN DEL SERVIDOR
# --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
