# routes/auth.py
from flask import Blueprint, request, render_template, redirect, url_for, flash,make_response
from db.db_config import get_db_connection
from models.logUsuario import User 
from flask_login import login_user, logout_user, current_user
from models.usuario import Usuario
import bcrypt

auth_bp = Blueprint('auth', __name__)


#Protejo a todas las rutas para que solamente se acceda si el usuario esta logeado
@auth_bp.before_request
def require_login():
     if not current_user.is_authenticated and request.endpoint != 'auth.login':
        return redirect(url_for('auth.login'))  


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        logout_user()  # Cierra la sesión si el usuario ya está autenticado
        flash('Sesión cerrada automáticamente. Por favor, inicie sesión nuevamente.', 'info')
        return redirect(url_for('auth.login'))  # Redirige a login después de cerrar la sesión
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        db = get_db_connection()
        usuario_data = Usuario.obtener_por_nombre(nombre, db)
        db.close()

        if usuario_data and bcrypt.checkpw(password.encode('utf-8'), usuario_data[2].encode('utf-8')):
            user = User(usuario_data[0], usuario_data[1])  # Crear objeto de usuario
            login_user(user)  # Iniciar sesión
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos','danger')
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
    


@auth_bp.route('/logout')
def logout():
    logout_user()  # Cerrar sesión
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))  # Redirigir al login

@auth_bp.route('/prueba')
def prueba():
    return render_template('prueba.html')
    
    
    





