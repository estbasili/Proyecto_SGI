--  Propuesta de Estructura del proyecto

tu_proyecto/              #Directorio raiz del proyecto
├── app.py                #Punto de entrada de la aplicacion Flask
├── db/                   #configuracion de la base de datos para la conexion
│   └── db_config.py  
|   
├── settings/             #Valores para prueba de la DB
│   └── datos_prueba.sql
│   └── gestion.sql 
| 
├── models/               #Modelos de datos de la aplicacion
│   └── __init__.py
│   └── logUsuario.py     # modelo de clase user para ususario que inicio sesion
|   └── usuario.py        # modelo de clase ususario
|
├── static/               #Estilos para las planillas
│   └── common/
|        ├── assents
|        ├── css
│        └── js
│       
├── templates/            #Plantillas HTML
│   ├── login.html
│   └── index.html        # plantilla principal Home
|
├── routes/               #Directorio que contiene las rutas de la aplicacion
│   └── __init__.py
│   └── auth.py 
|
├── requirements.txt 
└── README.md 

# Proyecto Flask

Repositorio 

## Requisitos

Se requieren los siguientes programas para la ejecución del proyecto:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

## Instalación

### 1. Clonar el repositorio

Abrir una terminal y ejecutar el comando:

```bash
git clone https://github.com/CarlosDevUni/proyecto_flask
```

### 2. Navegar al directorio del proyecto

```bash
cd proyecto_flask
```

### 3. Crear un entorno virtual

En **Windows**:

```bash
py -3 -m venv .venv
```

En **macOS/Linux**:

```bash
python3 -m venv .venv
```

### 4. Activar el entorno virtual

En **Windows**:

```bash
.venv\Scripts\activate
```

En **macOS/Linux**:

```bash
source .venv/bin/activate
```

### 5. Instalar las dependencias

Las dependencias necesarias se encuentran en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 6. Ejecutar el proyecto

```bash
python main.py
```

## Estructura del Proyecto

```
├── api/
│   ├── __init__.py
│   ├── db/
│       └── test_db.py
├── main.py
├── .venv/
├── requirements.txt
└── README.md
```

- `api/`: Carpeta principal del código fuente de la aplicación.
- `main.py`: Archivo de inicio de la aplicación
- `requirements.txt`: Archivo que contiene las dependencias del proyecto.
- `.venv/`: Entorno virtual (esta carpeta está en `.gitignore` y no debe ser incluida en el repositorio).