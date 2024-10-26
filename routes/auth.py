# routes/auth.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from db.db_config import get_db_connection
from models.logUsuario import User # Importar la clase User desde models.py
from flask_login import login_user, logout_user
from models.usuario import Usuario
import bcrypt

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()  # Cerrar sesión
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))  # Redirigir al login
    





