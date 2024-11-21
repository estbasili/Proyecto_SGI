from api.db.db import get_db_connection, DBError
from werkzeug.security import generate_password_hash, check_password_hash # para manejer el hasheo
import jwt
import datetime
from api import app


app.config['SECRET_KEY'] = "clave_app"

class Usuario:
    schema = {
        "nombre": str,
        "email": str,
        "contraseña": str,
        "id_rol": int
    }

    @classmethod
    def validar_datos(cls, data):
        
        if data == None or type(data) != dict:
             
             return False
        for key in cls.schema:
            if key not in data:
                print(data)
                return False
            if type(data[key]) != cls.schema[key]:
                return False
        return True


    def __init__(self, data):
        self.id_usuario = data[0]
        self.nombre = data[1]
        self.email = data[2]
        self.contraseña = data[3]
        self.id_rol = data[4] 


    def a_json(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            # "contraseña": self.contraseña,
            # "id_rol": self.id_rol,
        }
    

    ########################################################################### para el registro de usuario

    @classmethod
    def register(cls, data):

        print (type (data))

        if not cls.validar_datos(data):
            raise DBError({"message": "Campos/valores inválidos", "code": 400})
        
        nombre = data ["nombre"]
        email = data["email"]
        contraseña = data["contraseña"]
        id_rol = data["id_rol"]


        # Buscar si existe un usuario con el mismo nombre
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id_usuario FROM usuario WHERE email = %s', (email,))
        row = cursor.fetchone()


        if row is not None:
            raise DBError({"message": "Ya existe un usuario con ese nombre", "code": 400})
        
        # Generar el hash de la contraseña
        hashed_password = generate_password_hash(contraseña, method='pbkdf2:sha256')
        
        print(nombre, email, hashed_password, id_rol)
        # Guardar el usuario en la base de datos con la contraseña hasheada        
        cursor.execute('INSERT INTO usuario (nombre, email, contraseña, id_rol) VALUES (%s, %s, %s, %s)', (nombre, email, hashed_password, id_rol))
        connection.commit()


        """ obtener el id del registro creado """
        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]


        # Recuperar el objeto creado
        print (id)
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id, ))
       
        nuevo = cursor.fetchone()
        print (nuevo)
        cursor.close()
        connection.close()
        
        return Usuario(nuevo).a_json()


    ############################################################################ para realzar el logeo

    @classmethod
    def login(cls, auth): # auth como abreviatura de autorizacion que es el espacio donde se guarda, el nombre y pass va a venir en una cabezera especial aut
        
        if not auth or not auth.email or not auth.password:
            raise DBError({"message": "No autorizado", "code": 401})


        connection = get_db_connection()
        cursor = connection.cursor()
        # Buscar el usuario por nombre de usuario
        cursor.execute('SELECT id_usuario, email, password FROM usuario WHERE email = %s', (auth.email,))# buscamos donde cohincide el nombre de usuario
        row = cursor.fetchone()


        # row[2] contiene el hash de la contraseña para saber si la contraseña coincie con la transformacion de la contraseña que estamos recibiendo desde el front
        if not row or not check_password_hash(row[2], auth.password): 
            raise DBError({"message": "No autorizado", "code": 401})


        # Obtener la hora actual en UTC y convertirla a un timestamp
        exp_timestamp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)).timestamp()# define cuanto tiempo es valido ese token, en este caso es 1 minuto
        
        # Generar token JWT se devuelve si el usuario que inicio el login es verdadero 
        token = jwt.encode({
            'email': auth.email,
            'id_usuario': row[0],
            'exp': exp_timestamp
        }, app.config['SECRET_KEY'], algorithm = "HS256")
        return {"token": token, "email": auth.email, "id_usuario": row[0]}


############################################################ otras funciones 


    @classmethod
    def get_all(cls):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, email, contraseña, id_rol FROM usuario")
        
        usuarios = []
        for usuario in cursor.fetchall():
            usuarios.append({
                "id_usuario": usuario[0],
                "nombre": usuario[1],
                "email": usuario[2],
                "contraseña": usuario[3],
                "id_rol": usuario[4],
            })

        cursor.close()
        conexion.close()
        return usuarios

    @classmethod
    def get_by_id(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if data:
            return Usuario(data).a_json()
        raise DBError('No existe el recurso solicitado')

    #@classmethod
    #def create(cls, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Control si el email no esta en uso por otro usuario
        email = data["email"]
        cursor.execute('SELECT * FROM usuario WHERE email = %s', (email,))
        row = cursor.fetchone()
        if row is not None:
            raise DBError("Email ya registrado")
        
        cursor.execute(
            "INSERT INTO usuario (nombre, email, contraseña, id_rol) VALUES (%s, %s, %s, %s)",
            (data['nombre'], data['email'], data['contraseña'], data['id_rol'])
        )
        conexion.commit()
        id_usuario = cursor.lastrowid
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario creado exitosamente", "id_usuario": id_usuario}

    #@classmethod
    #def update(cls, id, data):
        if not cls.validar_datos(data):
            raise DBError("Campos/valores inválidos")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute(
            "UPDATE usuario SET nombre = %s, email = %s, contraseña = %s, id_rol = %s WHERE id_usuario = %s",
            (data['nombre'], data['email'], data['contraseña'], data['id_rol'], id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario actualizado"}

    #@classmethod
    #def delete(cls, id):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        if cursor.fetchone() is None:
            raise DBError("No existe el recurso solicitado")
        cursor.execute('DELETE FROM usuario WHERE id_usuario = %s', (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Usuario eliminado"}
