CREATE DATABASE progreso2;
USE progreso2;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO products (producto, precio, stock) VALUES
('Laptop Dell XPS 13', 999.99, 50),
('Computadora HP Pavilion', 799.99, 30),
('Monitor Samsung 27"', 299.99, 40),
('Mouse Logitech MX Master 3', 99.99, 100),
('Teclado mecánico Razer', 129.99, 70);