CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    check_in DATE,
    check_out DATE
);

INSERT INTO reservas (check_in, check_out) VALUES
('2023-03-01', '2023-03-02'),
('2023-03-04', '2023-03-08');
