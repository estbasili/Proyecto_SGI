from flask import Flask, render_template, redirect, url_for, make_response,flash
from flask_login import LoginManager, login_required

from routes.auth import auth_bp
from models.logUsuario import User

app = Flask(__name__)
app.secret_key = 'clave_secreta'                          # clave secreta para firmar las cookies de sesion
app.register_blueprint(auth_bp)                           # se registran las rutas para que sean accesibles por la APP


# Inicializa Flask-Login inicializacion del sistema de autentificacion
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 

# recupero el usuario que inicio sesion
@login_manager.user_loader
def load_user(user_id):
     return User.get_by_id(user_id)

# Redirige siempre al login cuando la aplicación comienza
@app.route('/')
def home():
     return redirect (url_for('auth.login'))  
          
@login_manager.unauthorized_handler
def unauthorized():
    flash('Por favor, inicia sesión para acceder a esta página.', 'secondary')  # Personaliza el mensaje
    return redirect(url_for('auth.login'))  # Redirigir al login

# Asegúrate de que el usuario esté autenticado para acceder a la pagina de la app
@app.route('/home')
@login_required                                         
def index():
  response = make_response(render_template('index.html'))
  # Desactiva la caché para que el navegador siempre solicite una nueva versión
  response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '-1'
  return response
   

if __name__ == '__main__':
    app.run(debug=True)