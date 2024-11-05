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

INSERT INTO categoria (nombre) VALUES 
('Bebidas'),
('Snacks'),
('Enlatados');

INSERT INTO producto (nombre, descripcion, precio, stock, id_categoria, id_usuario) VALUES 
('Coca-Cola', 'Gaseosa cola 500ml', 1.50, 50, 1, 1),
('Papas Fritas', 'Bolsa de papas fritas 200g', 1.00, 30, 2, 1),
('Atún en Lata', 'Lata de atún 120g', 2.50, 20, 3, 1);

INSERT INTO proveedor (nombre, telefono, email, id_usuario) VALUES 
('Proveedor Bebidas', '1111111', 'bebidas@example.com', 1),
('Proveedor Snacks', '2222222', 'snacks@example.com', 1),
('Proveedor Enlatados', '3333333', 'enlatados@example.com', 1);

INSERT INTO producto_proveedor (id_proveedor, id_producto) VALUES 
(1, 1),  -- Coca-Cola con Proveedor Bebidas
(2, 2),  -- Papas Fritas con Proveedor Snacks
(3, 3);  -- Atún en Lata con Proveedor Enlatados

INSERT INTO orden_compra (fecha_pedido, fecha_recepcion, estado, id_proveedor, id_usuario) VALUES 
('2024-10-01', '2024-10-03', 'Recibido', 1, 1),
('2024-10-05', '2024-10-07', 'Recibido', 2, 1),
('2024-10-10', NULL, 'Pendiente', 3, 1);

INSERT INTO detalle_orden (id_orden, id_producto, cantidad, precio_unitario) VALUES 
(1, 1, 10, 1.50),  -- Orden 1, Coca-Cola
(2, 2, 5, 1.00),   -- Orden 2, Papas Fritas
(3, 3, 15, 2.50);  -- Orden 3, Atún en Lata