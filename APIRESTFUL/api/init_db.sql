CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    contrasena VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    fecha_creacion DATE
);

CREATE TABLE IF NOT EXISTS habitaciones (
    id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE,
    capacidad INT,
    descripcion VARCHAR(255),
    servicios VARCHAR(255),
    precio_noche FLOAT,
    camas TINYINT,
    tamaño INT,
    vistas VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_habitacion INT,
    check_in DATE,
    check_out DATE,
    huespedes TINYINT,
    monto_total FLOAT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion) ON DELETE CASCADE
);

INSERT INTO habitaciones (nombre, capacidad, descripcion, servicios, precio_noche)VALUES
('Habitacion Suite', '10', 'Amplios ambientes separados con estilo y privacidad para experiencias únicas', '["Wi-Fi", "Restaurante", "Piscina", "Spa", "Aire Acondicionado", "Toallas"]', '450', '5', '70','mar'),
('Habitacion familiar', '5', 'Espacio amplio y cómodo para familias que buscan descanso y diversión', '["Wi-Fi", "Toallas"]', '120','3', '30','ciudad'),
('Habitacion super de lujo', '7', 'Máximo confort con vistas exclusivas y servicios de categoría internacional.', '["Wi-Fi", "Restaurante", "Piscina", "Aire Acondicionado", "Toallas"]', '260','4','60','mar'),
('Habitacion clasica', '2', 'Comodidad esencial con diseño simple y funcional para estancias prácticas.', '["Wi-Fi", "Aire Acondicionado", "Toallas"]', '90','1','25','ciudad'),
('Habitacion superior', '3', 'Más espacio y confort con detalles modernos que elevan la experiencia.', '["Wi-Fi", "Restaurante", "Aire Acondicionado", "Toallas"]', '140','2','35','piscina'),
('Habitacion de lujo', '4', 'Diseño elegante, confort superior y detalles premium para una estadía especial.', '["Wi-Fi", "Piscina", "Aire Acondicionado", "Toallas"]', '180','2','40','casino');

INSERT INTO usuarios (nombre, apellido, contrasena, email, fecha_creacion)VALUES 
('Dylan', 'Ruiz', 'pepito123', 'druiz@fi.uba.ar', '2025-8-13'),
('Cerbero', 'Diaz','holamundoi', 'cerbero@gmail.com', '2025-8-12');

INSERT INTO reservas (id_usuario, id_habitacion, check_in, check_out, huespedes, monto_total)VALUES
('1', '4', '2025-10-12', '2025-10-15', '1', '270'),
('2', '1', '2025-10-13', '2025-10-17', '1', '1800');









