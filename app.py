from flask import Flask, redirect, url_for, render_template, make_response,flash
from flask_login import LoginManager, login_required, current_user
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
# Configura el mensaje de inicio de sesión
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
# Redirige al login con un mensaje flash personalizado
@login_manager.unauthorized_handler
def unauthorized():
    flash('Debes iniciar sesión para acceder a esta página.', 'warning')  # Mensaje flash
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
     return User.get_by_id(user_id)

##--------------------------------- Descomentar el if para que se rediriga solo con autenticacion    --------------

@app.route('/')
def home():
    # Redirige a index si el usuario ya está autenticado
#    if current_user.is_authenticated:
    return redirect(url_for('index'))
#    return redirect(url_for('auth.login'))


##--------------------------------- Descomentar @ login_required para proteger home --------------------------------
@app.route('/home')
#@login_required
def index():
    response = make_response(render_template('index.html'))
    # Desactiva la caché para que el navegador siempre solicite una nueva versión
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)
