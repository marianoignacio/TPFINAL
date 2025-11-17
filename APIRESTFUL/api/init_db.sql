CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    contraseña VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    fecha_creacion DATE
);

CREATE TABLE IF NOT EXISTS habitaciones (
    id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE,
    capacidad INT,
    descripcion VARCHAR(255),
    servicios VARCHAR(255),
    precio_noche FLOAT
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
('Habitacion Suite', '10', 'Amplios ambientes separados con estilo y privacidad para experiencias únicas', 'SERVICIOS', '450'),
('Habitacion familiar', '5', 'Espacio amplio y cómodo para familias que buscan descanso y diversión', 'SERVICIOS', '120'),
('Habitacion super de lujo', '7', 'Máximo confort con vistas exclusivas y servicios de categoría internacional.', 'SERVICIOS', '260'),
('Habitacion clasica', '2', 'Comodidad esencial con diseño simple y funcional para estancias prácticas.', 'SERVICIOS', '90'),
('Habitacion superior', '3', 'Más espacio y confort con detalles modernos que elevan la experiencia.', 'SERVICIOS', '140'),
('Habitacion de lujo', '4', 'Diseño elegante, confort superior y detalles premium para una estadía especial.', 'SERVICIOS', '180');

INSERT INTO usuarios (nombre, apellido, contraseña, email, fecha_creacion)VALUES 
('Dylan', 'Ruiz', 'pepito123', 'druiz@fi.uba.ar', '2025-8-13'),
('Cerbero', 'Diaz','holamundoi', 'cerbero@gmail.com', '2025-8-12');

INSERT INTO reservas (id_usuario, id_habitacion, check_in, check_out, huespedes, monto_total)VALUES
('1', '4', '2025-10-12', '2025-10-15', '1', '270'),
('2', '1', '2025-10-13', '2025-10-17', '1', '1800');









