-- Usuario en localhost --
-- Crear un nuevo usuario con una contraseña segura
CREATE USER 'gestion_user'@'localhost' IDENTIFIED BY 'gestion_inventario';

-- Conceder todos los privilegios en la base de datos 
GRANT ALL PRIVILEGES ON flask_app_db.* TO 'gestion_user'@'localhost' WITH GRANT OPTION;

-- Aplicar los cambios de privilegios (no es obligatorio en versiones modernas de MySQL)
-- FLUSH PRIVILEGES;

-- Verificar los privilegios del nuevo usuario
SHOW GRANTS FOR 'gestion_user'@'localhost';

-- Usuario en 127.0.0.1 -- (Esto permite acceder tanto con localhost como la dirección IPv4)
-- Crear un nuevo usuario con una contraseña segura
CREATE USER 'gestion_user'@'127.0.0.1' IDENTIFIED BY 'gestion_inventario';

-- Conceder todos los privilegios en la base de datos 
GRANT ALL PRIVILEGES ON flask_app_db.* TO 'gestion_user'@'127.0.0.1' WITH GRANT OPTION;

-- Aplicar los cambios de privilegios (no es obligatorio en versiones modernas de MySQL)
-- FLUSH PRIVILEGES;

-- Verificar los privilegios del nuevo usuario
SHOW GRANTS FOR 'gestion_user'@'127.0.0.1';