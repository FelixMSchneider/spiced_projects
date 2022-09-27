--   Throughout the week write SQL queries to answer the questions below
-- 1)        Get the names and the quantities in stock for each product.
SELECT product_name,units_in_stock FROM products ORDER BY units_in_stock DESC


-- 2)        Get a list of current products (Product ID and name).
SELECT product_id,product_name FROM products WHERE discontinued = FALSE;

-- 3)        Get a list of the most and least expensive products (name and unit price).
SELECT product_id, product_name,unit_price from products ORDER BY unit_price LIMIT 10;
SELECT product_id, product_name,unit_price from products ORDER BY unit_price DESC LIMIT 10;

-- 4)        Get products that cost less than $20.
SELECT product_id, product_name,unit_price from products WHERE unit_price > 20 ORDER BY unit_price;

-- 5)        Get products that cost between $15 and $25.
SELECT product_id, product_name, unit_price from products WHERE unit_price < 25 AND unit_price > 15;

-- 6)        Get products above average price.
SELECT product_name, unit_price FROM products WHERE unit_price > (SELECT AVG(unit_price) FROM products);

-- 7)        Find the ten most expensive products.
SELECT product_id, product_name,unit_price from products ORDER BY unit_price DESC LIMIT 10;


-- 8)        Get a list of discontinued products (Product ID and name).
SELECT product_name, unit_price FROM products WHERE discontinued = TRUE;


-- 9)        Count current and discontinued products.
SELECT COUNT(product_id) FROM products WHERE discontinued = TRUE;
SELECT COUNT(product_id) FROM products WHERE discontinued = FALSE;

SELECT discontinued, COUNT(product_id) FROM products GROUP BY discontinued;


-- 10)        Find products with less units in stock than the quantity on order.

SELECT p.product_id, p.product_name, od.quantity, p.units_in_stock FROM products p JOIN order_details od ON p.product_id = od.product_id WHERE p.units_in_stock < od.quantity;

-- 11)        Find the customer who had the highest order amount

SELECT c.customer_id,c.company_name, round(SUM(quantity*unit_price * (1-discount))) 
FROM order_details od 
JOIN orders o     ON   od.order_id = o.order_id  
JOIN customers c  ON o.customer_id = c.customer_id 
GROUP BY c.customer_id 
ORDER BY SUM(quantity*unit_price * (1-discount)) DESC LIMIT 1;


-- 12)        Get orders for a given employee and the according customer


-- 13)        Find the hiring age of each employee


-- 14)        Create views and/or named queries for some of these queries

