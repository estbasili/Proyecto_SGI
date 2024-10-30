# routes/auth.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
from db.db_config import get_db_connection
from models.logUsuario import User
from flask_login import login_user, logout_user, current_user
from models.usuario import Usuario
import bcrypt

auth_bp = Blueprint('auth', __name__)

# Protejo a todas las rutas para que solamente se acceda si el usuario está logueado
@auth_bp.before_request
def require_login():
    # Permite el acceso a la ruta de login y logout sin requerir autenticación
    if request.endpoint in ['auth.login', 'auth.logout']:
        return  # Permitir acceso sin redirección

    # Redirige a la página de inicio de sesión si el usuario no está autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

# Ruta de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirige a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Si el usuario envía los datos del formulario (método POST), intenta autenticarlo
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica las credenciales del usuario en la base de datos
        db = get_db_connection()
        usuario_data = Usuario.obtener_por_email(email, db)
        db.close()

        if usuario_data and bcrypt.checkpw(password.encode('utf-8'), usuario_data[3].encode('utf-8')):
            user = User(usuario_data[0], usuario_data[1])  # Crear objeto de usuario logeado
            login_user(user)  # Iniciar sesión
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    # Renderiza la página de inicio de sesión en caso de solicitud GET o fallo de autenticación
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))

