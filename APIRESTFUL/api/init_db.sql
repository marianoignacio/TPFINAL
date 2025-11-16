CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    contraseña VARCHAR(255),
    email VARCHAR(255),
    fecha_creacion DATE
);

CREATE TABLE IF NOT EXISTS habitaciones (
    id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
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

INSERT INTO reservas (check_in, check_out) VALUES
('2023-03-01', '2023-03-02'),
('2023-03-04', '2023-03-08');
