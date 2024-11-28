# Proyecto SGI (Sistema de Gestión de Inventario)

## Acerca del Proyecto Académico
Este proyecto fue desarrollado por estudiantes de la Universidad Provincial del Sudoeste (UPSO) como parte de la materia Proyecto Informático. Para la mayoría del equipo, este proyecto representó el trabajo final de la carrera, en el cual aplicamos los conocimientos adquiridos a lo largo de nuestra formación, integrando herramientas y conceptos de diversas materias.

## Equipo de Desarrollo
El equipo estuvo compuesto por tres integrantes, quienes colaboraron de manera activa en distintas áreas del desarrollo del proyecto:

De Prada Boris, Esteban Basili, Dana Fernández.

## Objetivo del Proyecto

[API RESTful para Gestión de Inventario]
Esta API está diseñada para gestionar un sistema de inventario. Los recursos principales incluyen productos, proveedores, categorías y usuarios. La API utiliza Flask y conecta con una base de datos SQL para almacenar los datos.
El SGI fue diseñado para ofrecer una solución de organización y control de inventarios para pequeños y medianos negocios. Este sistema integra funcionalidades como:

-Gestión de productos y categorías.
-Control de stock con generación de alertas.
-Administración de proveedores.
-Registro y seguimiento de órdenes de compra.
-Generación de reportes detallados.

## Tecnologías Utilizadas
Backend: Flask (Python)
Base de Datos: MySQL
Frontend: HTML, CSS, JavaScript
Herramientas: XAMMP, VS Code


# Instalación
## Requisistos
Se requieren los siguientes programas para la ejecución del proyecto:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### 1. Clonar el repositorio

Abrir una terminal y ejecutar el comando:

```bash
git clone https://github.com/estbasili/Proyecto_SGI
```

### 2. Navegar al directorio del proyecto

```bash
cd Proyecto_SGI
```
### 3. Crear una carpeta backend
```bash
mkdir backend
cd backend
```
### 4. Crear un entorno virtual

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

### 5. Instalar las dependencias del backend

Las dependencias necesarias se encuentran en settings/requirements.txt:

```bash
pip install -r settings/requirements.txt

```

### 6. Inicializar la base de datos

Es fundamental crear la base de datos antes de ejecutar el proyecto. El script necesario se encuentra en `settings/gestion.sql`. Este archivo contiene todas las definiciones de tablas y relaciones necesarias para el sistema.

Para ejecutar el script, puedes usar phpMyAdmin o el cliente MySQL desde la línea de comandos:

```bash
mysql -u root -p < settings/gestion.sql
```

También puedes copiar y pegar el contenido del archivo en la pestaña SQL de phpMyAdmin.

### Notas Importantes: Configuración del entorno

Antes de ejecutar el proyecto, asegúrate de configurar correctamente las siguientes **variables de entorno** en un archivo `.env` en el directorio raíz del proyecto:

```plaintext
DB_NAME=nombre_base_datos
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

### 6. Ejecutar el proyecto

```bash
python app.py
```

##  Propuesta de Estructura del proyecto

```
Proyecto_SGI/
├── backend/
│   ├── api/
│   │   ├── db/
|   |   |    └── bd.py
│   │   ├── models/
│   │   │       ├── categoria.py
│   │   │       ├── detalle_orden.py
│   │   │       ├── orden.py
│   │   │       ├── producto.py
│   │   │       ├── proveedor.py
│   │   │       └── usuario.py
│   │   ├── routes/
│   │   │   ├── categoria.py
│   │   │   ├── orden.py
│   │   │   ├── producto.py
│   │   │   ├── proveedor.py
│   │   │   └── usuario.py
│   │   ├─── utils/
│   │   |    └── security.py     # Funciones de utilidad para seguridad
|   |   └─ __init__.py
│   └─ app.py                    # Archivo principal del backend
|
├── doc/                         # Archivos con las imagenes de los diagramas de clase 
|
├── frontend/
│   ├── assets/                  # Imágenes y recursos estáticos
│   │   ├── favicon.ico
│   │   ├── imagen_fondo.png
│   │   └── usuario.png
│   ├── css/                     # Archivos CSS personalizados
│   │   ├── dist/                # archivos de bootstrap 4
|   |   ├── plugins/
|   |   └── personalizado/
|   |             └─ estilos.css # archivo de estilos propios del proyecto
│   ├── js/                      # Archivos JavaScript personalizados
│   |   ├── admin/
|   |   |      └─ scripts.js     # JavaScript para manejar la pagina principal
|   |   ├── common/
|   │   |      └─ common.js
|   |   └─ user/
|   |        └─ login_register.js # JavaScript para manejo de loginy registro 
|   |
│   ├── index.html                # Página principal
│   └── login-register.html       # Página de inicio de sesión
|
├── settings/
│   ├── creacion_usuario.sql      # Scripts SQL para configuración inicial
│   ├── datos_prueba.sql          # Datos de prueba
│   ├── gestion.sql               # Tablas y relaciones
│   └─ requirements.txt           # Dependencias necesarias para el backend
|
├── .env                          # Variables de entorno
├── .gitignore                    # Archivos/carpetas a ignorar en Git
└── README.md                     # Documentación del proyecto

models/: Contiene las definiciones de los modelos de datos (proveedor.py, categoria.py, etc.).
routes/: Contiene las rutas para los endpoints de la API (proveedor.py, categoria.py, etc.).
utils/: Contiene funciones de utilidad, como la autenticación de usuarios.
```

## Documentación de la API

### Autenticación
La API utiliza autenticación basada en tokens JWT. Para acceder a los endpoints protegidos, se debe incluir el token en el header:

```bash
Authorization: Bearer <token>
```

### Recursos Disponibles

#### 1. Usuarios
**Endpoint Base**: `/usuarios`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/usuarios` | Obtiene lista de todos los usuarios | No |
| GET | `/usuarios/:id` | Obtiene un usuario específico | No |
| POST | `/register` | Registra un nuevo usuario | No |

#### 2. Productos
**Endpoint Base**: `/usuarios/:id_usuario/productos`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/productos` | Obtiene todos los productos del usuario | Sí |
| GET | `/productos/:id` | Obtiene un producto específico | Sí |
| POST | `/productos` | Crea un nuevo producto | Sí |
| PUT | `/productos/:id` | Actualiza un producto existente | Sí |
| DELETE | `/productos/:id` | Elimina un producto | Sí |
| GET | `/proveedores/:id_producto` | Obtiene proveedores de un producto | Sí |

#### 3. Proveedores
**Endpoint Base**: `/usuarios/:id_usuario/proveedores`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/proveedores` | Obtiene todos los proveedores | Sí |
| POST | `/proveedores` | Crea un nuevo proveedor | Sí |
| PUT | `/proveedores/:id` | Actualiza un proveedor | Sí |
| DELETE | `/proveedores/:id` | Elimina un proveedor | Sí |
| GET | `/listarProveedores` | Lista completa de proveedores | Sí |

#### 4. Órdenes
**Endpoint Base**: `/usuarios/:id_usuario/ordenes`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/ordenes` | Obtiene todas las órdenes del usuario | Sí |
| GET | `/ordenes/:id` | Obtiene una orden específica | Sí |

#### 5. Categorías
**Endpoint Base**: `/usuarios/:id_usuario/categorias`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/categorias` | Obtiene todas las categorías del usuario | Sí |
| GET | `/categorias/:id` | Obtiene una categoría específica | Sí |
| POST | `/categorias` | Crea una nueva categoría | Sí |
| PUT | `/categorias/:id` | Actualiza una categoría existente | Sí |
| DELETE | `/categorias/:id` | Elimina una categoría | Sí |

#### 6. Estados de Órdenes
**Endpoint Base**: `/estados`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/estados` | Obtiene todos los estados posibles | No |

### Estados Disponibles
- **Pendiente**: Estado inicial de una orden de compra
- **Completado**: Estado final cuando la orden se ha procesado completamente

### Ejemplos de Uso

#### 1. Registro de Usuario
```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Usuario Ejemplo",
    "email": "usuario@ejemplo.com",
    "contraseña": "contraseña123",
    "id_rol": 1
  }'
```

#### 2. Crear un Producto
```bash
curl -X POST http://localhost:5001/usuarios/1/productos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Producto Nuevo",
    "descripcion": "Descripción del producto",
    "precio": 99.99,
    "stock": 100,
    "categoria_id": 1
  }'
```

#### 3. Obtener Proveedores
```bash
curl -X GET http://localhost:5001/usuarios/1/proveedores \
  -H "Authorization: Bearer <token>"
```

#### 4. Crear una Categoría
```bash
curl -X POST http://localhost:5001/usuarios/1/categorias \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Electrónicos",
    "descripcion": "Productos electrónicos y accesorios"
  }'
```

#### 5. Obtener Categorías del Usuario
```bash
curl -X GET http://localhost:5001/usuarios/1/categorias \
  -H "Authorization: Bearer <token>"
```

### Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado exitosamente |
| 400 | Error en la solicitud |
| 401 | No autorizado |
| 404 | Recurso no encontrado |
| 500 | Error interno del servidor |

### Notas Importantes
- Todos los endpoints (excepto registro y login) requieren autenticación mediante token JWT
- Los IDs de usuario en las rutas deben corresponder al usuario autenticado
- Las respuestas son en formato JSON
- Para operaciones de creación y actualización, los datos deben enviarse en formato JSON en el cuerpo de la solicitud
- Todas las operaciones de categorías requieren autenticación mediante token JWT
- Las categorías están asociadas a un usuario específico
- Al eliminar una categoría, se debe considerar la integridad referencial con los productos asociados
```

