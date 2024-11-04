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
├── frontend/
     ├── admin/
     │   ├── index.html                
     │   │
     │   └── js/
     │        └── script.js 
     ├── assents/
     │   ├── favico.ico              
     │   └── usuario.png 
     │    
     ├── common/
     │   └── js/
     │       ├──dist/
     │       │                     
     │       └── plugins/
     │                   
             
