CREATE DATABASE inventory_management;
USE inventory_management;

-- User table for authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
SELECT * FROM users

-- Products table for inventory management
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2)
);
SELECT * FROM products

-- Sales table to track each sale
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity_sold INT,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
SELECT * FROM sales


-- Inventory Summary View (virtual table) for cost calculations
CREATE VIEW inventory_summary AS
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.quantity,
    p.price,
    (p.quantity * p.price) AS total_value
FROM products p;

SELECT * FROM inventory_summary;
