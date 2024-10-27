from flask import Flask, render_template
from flask_login import LoginManager, login_required
from routes.auth import auth_bp
from models.logUsuario import User

app = Flask(__name__)
app.secret_key = 'clave_secreta'                          # clave secreta para firmar las cookies de sesion
app.register_blueprint(auth_bp)                           # se registran las rutas para que sean accesibles por la APP


# Inicializa Flask-Login inicializacion del sistema de autentificacion
login_manager = LoginManager()
login_manager.init_app(app)

# recupero el usuario que inicio sesion
@login_manager.user_loader
def load_user(user_id):
     return User.get_by_id(user_id)

@app.route('/')
@login_required                                           # Asegúrate de que el usuario esté autenticado para acceder a la pagina
def index():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True)