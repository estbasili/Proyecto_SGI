--  Propuesta de Estructura del proyecto

tu_proyecto/              #Directorio raiz del proyecto
├── app.py                #Punto de entrada de la aplicacion Flask
├── db/                   #configuracion de la base de datos para la conexion
│   └── config_db.py      #configuracion del conector de la base de datos
├── settings/             #Valores para prueba de la DB
│   └── datos_prueba.sql
│   └── gestion.sql  
├── models/               #Modelos de datos de la aplicacion
│   └── __init__.py
│   └── logUsuario.py     #me sirve para recuperar el ususario que inicio sesion
|   └── usuario.py
├── static/               #Estilos para las planillas
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── templates/            #Plantillas HTML
│   ├── login.html
│   └── index.html
├── routes/               #Directorio que contiene las rutas de la aplicacion
│   └── __init__.py
│   └── auth.py 
├── requirements.txt              