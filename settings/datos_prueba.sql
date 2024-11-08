-- Insertar roles en la tabla rol
INSERT INTO rol (nombre)
VALUES
('Usuario'),
('Usuario'),
('Usuario');

-- Insertar usuarios en la tabla usuario
INSERT INTO usuario (nombre, email, contraseña, id_rol)
VALUES
('Boris De Prada','boris@gmail.com','$2b$12$Cu.IC6FSBQHcZdtqSeWkQOaYs7T7PxeXjmPImxhKnNMAV9FPH4p0O', 4),
('Dana Fernandez','dana@gmail.com','$2b$12$Q/vigzlPS8zXttV3c0kz/ecTyiHrS0W7UstgdVHmC59Z3oLHN8z42', 5),
('Esteban Basilli','esteban@gmail.com','$2b$12$8JHo7jFcN2Nz72lN3FZMlOEJVQ9IpcPKVPr4PXZypR.vedwlrPI9S', 6);

INSERT INTO categoria (nombre) VALUES 
('Bebidas'),
('Snacks'),
('Enlatados');

INSERT INTO producto (nombre, descripcion, precio, stock, id_categoria, id_usuario) VALUES 
('Coca-Cola', 'Gaseosa cola 500ml', 1.50, 50, 201, 10),
('Papas Fritas', 'Bolsa de papas fritas 200g', 1.00, 30, 202, 11),
('Atún en Lata', 'Lata de atún 120g', 2.50, 20, 203, 12);

INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES 
('Proveedor Bebidas', '1111111', 'bebidas@example.com', 10),
('Proveedor Snacks', '2222222', 'snacks@example.com', 11),
('Proveedor Enlatados', '3333333', 'enlatados@example.com', 12);

INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES 
(6, 18),  -- Coca-Cola con Proveedor Bebidas
(7, 18),  -- Papas Fritas con Proveedor Snacks
(8, 19);  -- Atún en Lata con Proveedor Enlatados

INSERT INTO orden_compra (fecha_pedido, fecha_recepcion, estado, id_proveedor, id_usuario) VALUES 
('2024-10-01', '2024-10-03', 'Recibido', 6, 10),
('2024-10-05', '2024-10-07', 'Recibido', 7, 11),
('2024-10-10', NULL, 'Pendiente', 8, 12);

INSERT INTO detalle_orden (id_orden, id_producto, cantidad, precio_unitario) VALUES 
(1, 17, 10, 1.50),  -- Orden 1, Coca-Cola
(2, 18, 5, 1.00),   -- Orden 2, Papas Fritas
(3, 19, 15, 2.50);  -- Orden 3, Atún en Lata