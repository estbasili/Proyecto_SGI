from flask import Flask, session, render_template,redirect,url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from routes.auth import auth_bp
from models.logUsuario import User
app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(auth_bp)

##
# Inicializa Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Carga el usuario por ID
@login_manager.user_loader
def load_user(user_id):
    # Aquí debes recuperar el usuario de la base de datos usando el user_id
    return User.get_by_id(user_id)
##


@app.route('/')
@login_required  # Asegúrate de que el usuario esté autenticado
def index():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True)