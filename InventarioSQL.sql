CREATE DATABASE inventario;

USE inventario;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE ordenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    product_image VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES productos(id)
);

CREATE TABLE facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    fecha DATE,
    total DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES ordenes(id)
);


INSERT INTO productos (product_name, price, stock) VALUES
('Laptop Dell XPS 13', 999.99, 50),
('Computadora HP Pavilion', 799.99, 30),
('Monitor Samsung 27"', 299.99, 40),
('Mouse Logitech MX Master 3', 99.99, 100),
('Teclado mecánico Razer', 129.99, 70);
