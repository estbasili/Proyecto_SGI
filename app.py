from flask import Flask, redirect, url_for
from flask_login import LoginManager
from routes.auth import auth_bp
from models.logUsuario import User

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Registrar el blueprint
app.register_blueprint(auth_bp)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
     return User.get_by_id(user_id)

@app.route('/')
def home():
     return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
