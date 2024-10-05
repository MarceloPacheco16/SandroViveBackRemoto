BEGIN;
USE db_django;

-- Tabla Categoria
CREATE TABLE `app_django_categoria` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(15) NOT NULL,
    `descripcion` VARCHAR(30) NOT NULL,
    `activo` INT NOT NULL
);

-- Tabla Producto
CREATE TABLE `app_django_producto` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(15) NOT NULL,
    `descripcion` VARCHAR(30) NOT NULL,
    `talle` VARCHAR(10) NOT NULL,
    `color` VARCHAR(15) NOT NULL,
    `precio` DECIMAL(10, 2) NOT NULL,
    `cantidad` INT NOT NULL,
    `cantidad_disponible` INT NOT NULL,
    `cantidad_limite` INT NOT NULL,
    `imagen` VARCHAR(100),
    `observaciones` TEXT,
    `activo` INT NOT NULL,
    `categoria_id` INT,
    FOREIGN KEY (`categoria_id`) REFERENCES `app_django_categoria` (`id`) ON DELETE SET NULL
);

-- Tabla Provincia
CREATE TABLE `app_django_provincia` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `descripcion` VARCHAR(60) NOT NULL
);

-- Tabla Localidad
CREATE TABLE `app_django_localidad` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `descripcion` VARCHAR(80) NOT NULL,  -- Ajustar la longitud según tus necesidades (por ejemplo, 80 caracteres)
    `provincia_id` INT,
    FOREIGN KEY (`provincia_id`) REFERENCES `app_django_provincia` (`id`) ON DELETE SET NULL
);

-- Tabla Usuario
CREATE TABLE `app_django_usuario` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(30) NOT NULL,
    `contrasenia` VARCHAR(128) NOT NULL,
    `cant_intentos` INT NOT NULL DEFAULT 0,
    `activo` INT NOT NULL DEFAULT 1
);

-- Tabla Cliente
CREATE TABLE `app_django_cliente` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(15) NOT NULL,
    `apellido` VARCHAR(15) NOT NULL,
    `telefono` VARCHAR(15) NOT NULL,
    `domicilio` VARCHAR(60) NOT NULL,
    `localidad` VARCHAR(80) NOT NULL,  -- Ajustar la longitud según tus necesidades (por ejemplo, 80 caracteres)
    `provincia` VARCHAR(60) NOT NULL,  -- Ajustar la longitud según tus necesidades (por ejemplo, 60 caracteres)
    `codigo_postal` VARCHAR(15) NOT NULL,
    `usuario_id` INT,
    `activo` INT NOT NULL,
    FOREIGN KEY (`usuario_id`) REFERENCES `app_django_usuario` (`id`) ON DELETE SET NULL
);

-- Tabla Empleado
CREATE TABLE `app_django_empleado` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(15) NOT NULL,
    `apellido` VARCHAR(15) NOT NULL,
    `rol` VARCHAR(15) NOT NULL,
    `usuario_id` INT,
    `activo` INT NOT NULL,
    FOREIGN KEY (`usuario_id`) REFERENCES `app_django_usuario` (`id`) ON DELETE SET NULL
);

-- Tabla Estado
CREATE TABLE `app_django_estado` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tipo_estado` VARCHAR(10) NOT NULL
);

-- Tabla Pedido
CREATE TABLE `app_django_pedido` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `cliente_id` INT,
    `fecha_creacion` DATE NOT NULL,
    `fecha_pactada` DATE NOT NULL,
    `fecha_entregada` DATE NOT NULL,
    `estado_id` INT,
    `total` DECIMAL(10, 2) NOT NULL,
    `observaciones` TEXT,
    FOREIGN KEY (`cliente_id`) REFERENCES `app_django_cliente` (`id`) ON DELETE SET NULL,
    FOREIGN KEY (`estado_id`) REFERENCES `app_django_estado` (`id`) ON DELETE SET NULL
);

-- Tabla Pedido_Producto
CREATE TABLE `app_django_pedido_producto` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `pedido_id` INT,
    `producto_id` INT,
    `cantidad` INT NOT NULL,
    `sub_total` DECIMAL(10, 2) NOT NULL,
    `total` DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (`pedido_id`) REFERENCES `app_django_pedido` (`id`) ON DELETE SET NULL,
    FOREIGN KEY (`producto_id`) REFERENCES `app_django_producto` (`id`) ON DELETE SET NULL
);

-- Tabla Factura
CREATE TABLE `app_django_factura` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `pedido_id` INT,
    `fecha_emision` DATE NOT NULL,
    `total` DECIMAL(10, 2) NOT NULL,
    `estado_pago` VARCHAR(20) DEFAULT 'Pendiente',
    `metodo_pago` VARCHAR(50),
    `observaciones` TEXT,
    FOREIGN KEY (`pedido_id`) REFERENCES `app_django_pedido` (`id`) ON DELETE SET NULL
);

-- Tabla Detalle_Envio
CREATE TABLE `app_django_detalle_envio` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `pedido_id` INT,
    `domicilio` VARCHAR(60) NOT NULL,
    `localidad` VARCHAR(80) NOT NULL,
    `provincia` VARCHAR(60) NOT NULL,
    `fecha_creacion` DATE NOT NULL,
    `observaciones` TEXT,
    FOREIGN KEY (`pedido_id`) REFERENCES `app_django_pedido` (`id`) ON DELETE SET NULL
);

COMMIT;