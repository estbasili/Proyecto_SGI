-- Insertar roles en la tabla rol
INSERT INTO rol (nombre)
VALUES
('Usuario'),
('Usuario'),
('Usuario');

-- Insertar usuarios en la tabla usuario
INSERT INTO usuario (nombre, email, contraseña, id_rol)
VALUES
('Boris De Prada','boris@gmail.com','$2b$12$Cu.IC6FSBQHcZdtqSeWkQOaYs7T7PxeXjmPImxhKnNMAV9FPH4p0O', 1),
('Dana Fernandez','dana@gmail.com','$2b$12$Q/vigzlPS8zXttV3c0kz/ecTyiHrS0W7UstgdVHmC59Z3oLHN8z42', 1),
('Esteban Basilli','esteban@gmail.com','$2b$12$8JHo7jFcN2Nz72lN3FZMlOEJVQ9IpcPKVPr4PXZypR.vedwlrPI9S', 1);

-- Insertar proveedores en la tabla proveedor
INSERT INTO `proveedor` (`id_proveedor`, `nombre`, `telefono`, `email`, `id_usuario`) 
VALUES ('2', 'frutas ecuatorianas limitada', '', '', '4');

-- Insertar productos en la tabla producto 
INSERT INTO `producto` (`id_producto`, `nombre`, `descripcion`, `precio`, `stock`, `id_categoria`, `id_usuario`) 
VALUES ('2', 'Banana', 'Fruta tropical', '120', '100', '1', '6');