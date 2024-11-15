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
Proyecto_SGI/
│
├── Backend/
|     └── api/ 
|         ├── db/
|         |   ├── __pycache__/
│         |   └── db_config.py
|         |
│         ├── models/
│         |      ├── __pycache__/
│         |      ├── categoria.py
│         |      ├── orden.py
│         |      ├── proveedor.py
│         |      ├── usuario.py                        
│         |      └── producto.py                    
│         | 
│         ├── node_modules/
│         |      └── dotenv
|         |
|         ├── routes/
│         |      ├── __pycache__/
│         |      ├── categoria.py
│         |      ├── orden.py
│         |      ├── proveedor.py
│         |      ├── usuario.py                        
│         |      └── producto.py 
|         ├── __init__.py                
|         └── app.py
|
├── setting/
│       ├── creacion_user.sql
│       ├── datos_prueba.sql
│       └── gestin.sql
│   
├── frontend/
|     ├── css/
|     |    ├── dist/
|     |    ├── personalizado/
|     |    |        └── estilos.css 
|     |    └── plugins/
|     | 
|     ├── assents/
|     │   ├── favico.ico
|     │   ├── imagen_login.jpg              
|     │   └── usuario.png 
|     │    
|     ├── js/
|     |    └── admin/
|     |    |    └── script.js
|     |    └── user/
|     |         └── login_register.js
|     |
|     ├── index.html                 
|     └── login-register.html
|
├── README.md                 
└── requirements.txt
