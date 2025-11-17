USE hotel;

CREATE TABLE productos(
ID INT AUTO_INCREMENT,
Nombre_producto VARCHAR(241),
Precio DECIMAL,
FechaDeCreacion DATETIME,
FechaDeModificacion DATETIME,
PRIMARY KEY(ID)
);

INSERT INTO productos
(Nombre_producto, Precio, FechaDeCreacion)
VALUES 
('cama',60, CURRENT_DATE());

