## Proyecto Gestor de Inventario

## Requisitos

Se requieren los siguientes programas para la ejecución del proyecto:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

## Instalación

### 1. Clonar el repositorio

Abrir una terminal y ejecutar el comando:

```bash
git clone https://github.com/estbasili/Proyecto_SGI
```

### 2. Navegar al directorio del proyecto

```bash
cd Proyecto_SGI
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
python app.py
```

##  Propuesta de Estructura del proyecto
```
tu_proyecto/
│
├── app.py                            # Archivo principal que inicia la aplicación Flask
│
├── db/
│   └── db_config.py                  # Configuración de la base de datos y conexión
│
├── models/
│   ├── __init__.py                   # Inicialización de módulo (puede estar vacío o con imports de modelos)
│   ├── logUsuario.py                 # Modelo relacionado con el inicio de sesión y usuarios logueados
│   └── usuario.py                    # Modelo relacionado con la entidad Usuario
│
├── routes/
│   ├── __init__.py                   # Inicialización de módulo (puede estar vacío o con imports de rutas)
│   └── auth.py                       # Rutas de autenticación y login (Blueprint)
│
├── settings/
│   ├── datos_prueba.sql              # Datos de prueba para la base de datos (si es necesario)
│   └── gestion.sql                   # Scripts SQL para la gestión de la base de datos
│
├── static/
│   ├── css/
│   │   └── styles.css                # Archivo de estilos CSS para la aplicación
│   │
│   └── js/
│       └── script.js                 # Archivo JavaScript para funcionalidades del lado del cliente
│
├── templates/
│   ├── index.html                    # Página principal de la aplicación
│   ├── login.html                    # Página de inicio de sesión
│   └── prueba.html                   # Página de prueba para autenticación (opcional)
│
└── __init__.py                       # Archivo de inicialización del paquete principal

``` 
### Descripción de cada archivo y carpeta

app.py: Archivo principal de la aplicación que registra los Blueprints, inicia la aplicación Flask, y configura la autenticación.

db/: Contiene el archivo de configuración de la base de datos (db_config.py).

models/: Incluye los modelos de la aplicación, como logUsuario.py para el manejo de usuarios autenticados y usuario.py para la entidad Usuario.

routes/: Contiene las rutas de la aplicación, incluyendo auth.py para la lógica de autenticación. La estructura con Blueprints ayuda a escalar la aplicación.

settings/: Carpeta para almacenar archivos de configuración o scripts SQL necesarios para la base de datos.

static/: Contiene los archivos estáticos como CSS y JavaScript, necesarios para el diseño y la funcionalidad del lado del cliente.

css/styles.css: Archivo CSS que centraliza los estilos de la aplicación.

js/script.js: Archivo para las funciones JavaScript que mejoran la experiencia del usuario.

templates/: Carpeta con las plantillas HTML utilizadas en la aplicación.

index.html: Página principal de la aplicación después de iniciar sesión.

login.html: Página de inicio de sesión, donde se incluye el archivo JavaScript.

prueba.html: Página de prueba de autenticación (si es necesario).

