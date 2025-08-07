-- CS4092 
-- author: Nekruz Ashrapov

CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

DROP TABLE IF EXISTS PURCHASE_ITEM;
DROP TABLE IF EXISTS PURCHASE;
DROP TABLE IF EXISTS CREDIT_CARD;
DROP TABLE IF EXISTS CUSTOMER;
DROP TABLE IF EXISTS PRODUCT;
DROP TABLE IF EXISTS STAFF;

-- 1. creating CUSTOMER table
CREATE TABLE CUSTOMER (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. creating CREDIT_CARD table
CREATE TABLE CREDIT_CARD (
    card_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    expiry_month INT NOT NULL CHECK (expiry_month BETWEEN 1 AND 12),
    expiry_year INT NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id) ON DELETE CASCADE
);

-- 3. creating STAFF table
CREATE TABLE STAFF (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0)
);

-- 4. creating PRODUCT table
CREATE TABLE PRODUCT (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    category VARCHAR(50),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. creating PURCHASE table
CREATE TABLE PURCHASE (
    purchase_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    card_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount > 0),
    status VARCHAR(20) DEFAULT 'completed',
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (card_id) REFERENCES CREDIT_CARD(card_id) ON DELETE RESTRICT
);

-- 6. creatijng PURCHASE_ITEM table
CREATE TABLE PURCHASE_ITEM (
    purchase_item_id INT PRIMARY KEY AUTO_INCREMENT,
    purchase_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (purchase_id) REFERENCES PURCHASE(purchase_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id) ON DELETE RESTRICT
);

-- creating indexes for better performance
CREATE INDEX idx_customer_email ON CUSTOMER(email);
CREATE INDEX idx_purchase_customer ON PURCHASE(customer_id);
CREATE INDEX idx_purchase_date ON PURCHASE(purchase_date);
CREATE INDEX idx_purchase_item_purchase ON PURCHASE_ITEM(purchase_id);
CREATE INDEX idx_purchase_item_product ON PURCHASE_ITEM(product_id);
CREATE INDEX idx_product_category ON PRODUCT(category);
CREATE INDEX idx_product_name ON PRODUCT(product_name);

-- some sample data

-- inserting CUSTOMERS
INSERT INTO CUSTOMER (first_name, last_name, email, phone, address, city, state, zip_code) VALUES
('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St', 'New York', 'NY', '10001'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90210'),
('Mike', 'Johnson', 'mike.johnson@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601'),
('Sarah', 'Wilson', 'sarah.wilson@email.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001'),
('David', 'Brown', 'david.brown@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001');

-- inserting CREDIT_CARDS
INSERT INTO CREDIT_CARD (customer_id, card_number, cardholder_name, expiry_month, expiry_year, card_type) VALUES
(1, '4111111111111111', 'John Doe', 12, 2027, 'Visa'),
(1, '5555555555554444', 'John Doe', 8, 2026, 'Mastercard'),
(2, '4000000000000002', 'Jane Smith', 10, 2028, 'Visa'),
(3, '3782822463100005', 'Mike Johnson', 6, 2027, 'American Express'),
(4, '6011111111111117', 'Sarah Wilson', 4, 2029, 'Discover'),
(5, '4111111111111111', 'David Brown', 11, 2026, 'Visa');

-- inserting STAFF
INSERT INTO STAFF (first_name, last_name, email, role, hire_date, salary) VALUES
('Alice', 'Manager', 'alice.manager@company.com', 'Store Manager', '2022-01-15', 75000.00),
('Bob', 'Assistant', 'bob.assistant@company.com', 'Sales Associate', '2022-06-01', 45000.00),
('Carol', 'Supervisor', 'carol.supervisor@company.com', 'Inventory Supervisor', '2021-11-20', 55000.00),
('Dan', 'Clerk', 'dan.clerk@company.com', 'Stock Clerk', '2023-03-10', 35000.00);

-- inserting PRODUCTS
INSERT INTO PRODUCT (product_name, description, price, stock_quantity, category) VALUES
('Wireless Headphones', 'High-quality Bluetooth headphones with noise cancellation', 149.99, 50, 'Electronics'),
('Running Shoes', 'Comfortable athletic shoes for running and training', 89.99, 75, 'Sports'),
('Coffee Maker', 'Programmable drip coffee maker with thermal carafe', 79.99, 30, 'Appliances'),
('Laptop Backpack', 'Durable backpack with padded laptop compartment', 45.99, 100, 'Accessories'),
('Smartphone Case', 'Protective case for iPhone with wireless charging support', 24.99, 200, 'Electronics'),
('Yoga Mat', 'Non-slip exercise mat for yoga and fitness', 29.99, 60, 'Sports'),
('Desk Lamp', 'LED desk lamp with adjustable brightness and USB charging port', 39.99, 40, 'Home'),
('Water Bottle', 'Insulated stainless steel water bottle, 32oz', 19.99, 150, 'Sports'),
('Bluetooth Speaker', 'Portable wireless speaker with waterproof design', 59.99, 80, 'Electronics'),
('Notebook Set', 'Pack of 3 ruled notebooks for office or school use', 12.99, 120, 'Office');


INSERT INTO PURCHASE (customer_id, card_id, total_amount, status) VALUES
(1, 1, 199.98, 'completed'),
(2, 3, 89.99, 'completed'),
(3, 4, 134.97, 'completed'),
(4, 5, 45.99, 'completed'),
(5, 6, 279.96, 'completed'),
(1, 2, 109.98, 'completed'),
(2, 3, 29.99, 'completed');

-- some fake data of customer purchases
INSERT INTO PURCHASE_ITEM (purchase_id, product_id, quantity, unit_price, subtotal) VALUES
-- Purchase 1: John Doe - Headphones + Smartphone Case
(1, 1, 1, 149.99, 149.99),
(1, 5, 2, 24.99, 49.99),

-- Purchase 2: Jane Smith - Running Shoes
(2, 2, 1, 89.99, 89.99),

-- Purchase 3: Mike Johnson - Coffee Maker + Yoga Mat + Water Bottle
(3, 3, 1, 79.99, 79.99),
(3, 6, 1, 29.99, 29.99),
(3, 8, 1, 19.99, 19.99),

-- Purchase 4: Sarah Wilson - Laptop Backpack
(4, 4, 1, 45.99, 45.99),

-- Purchase 5: David Brown - Bluetooth Speaker + Desk Lamp + Notebook Set
(5, 9, 2, 59.99, 119.98),
(5, 7, 1, 39.99, 39.99),
(5, 10, 1, 12.99, 12.99),

-- Purchase 6: John Doe - Yoga Mat + Water Bottle
(6, 6, 1, 29.99, 29.99),
(6, 8, 4, 19.99, 79.96),

-- Purchase 7: Jane Smith - Yoga Mat
(7, 6, 1, 29.99, 29.99);

-- updating product stock after purchases
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 1; -- Headphones
UPDATE PRODUCT SET stock_quantity = stock_quantity - 2 WHERE product_id = 5; -- Smartphone Case
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 2; -- Running Shoes
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 3; -- Coffee Maker
UPDATE PRODUCT SET stock_quantity = stock_quantity - 2 WHERE product_id = 6; -- Yoga Mat
UPDATE PRODUCT SET stock_quantity = stock_quantity - 5 WHERE product_id = 8; -- Water Bottle
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 4; -- Laptop Backpack
UPDATE PRODUCT SET stock_quantity = stock_quantity - 2 WHERE product_id = 9; -- Bluetooth Speaker
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 7; -- Desk Lamp
UPDATE PRODUCT SET stock_quantity = stock_quantity - 1 WHERE product_id = 10; -- Notebook Set

SELECT 'Database setup completed successfully!' as message;

-- to display table counts
SELECT 
    (SELECT COUNT(*) FROM CUSTOMER) as customers,
    (SELECT COUNT(*) FROM CREDIT_CARD) as credit_cards,
    (SELECT COUNT(*) FROM STAFF) as staff_members,
    (SELECT COUNT(*) FROM PRODUCT) as products,
    (SELECT COUNT(*) FROM PURCHASE) as purchases,
    (SELECT COUNT(*) FROM PURCHASE_ITEM) as purchase_items;

-- 1. i'm veryfing customers and their credit cards
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    COUNT(cc.card_id) as number_of_cards
FROM CUSTOMER c
    LEFT JOIN CREDIT_CARD cc ON c.customer_id = cc.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY customer_name;

-- 2. i'm verifying products by category
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    SUM(stock_quantity) as total_stock
FROM PRODUCT
GROUP BY category
ORDER BY category;

-- 3. here im verifying purchases with customer information
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) as customer,
    p.purchase_date,
    p.total_amount,
    COUNT(pi.purchase_item_id) as items_in_order
FROM CUSTOMER c
    JOIN PURCHASE p ON c.customer_id = p.customer_id
    JOIN PURCHASE_ITEM pi ON p.purchase_id = pi.purchase_id
GROUP BY p.purchase_id, c.customer_id, c.first_name, c.last_name, p.purchase_date, p.total_amount
ORDER BY p.purchase_date DESC;


SELECT 'E-commerce database setup completed successfully!' as status;