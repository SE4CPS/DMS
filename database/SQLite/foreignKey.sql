-- CREATE TABLE Product (
--     ProductId INTEGER PRIMARY KEY, 
--     ProductName VARCHAR(256) NOT NULL, 
--     ProductPrice DECIMAL NOT NULL, 
--     ProductCategory VARCHAR(256)
-- );

-- INSERT INTO Product VALUES (NULL, 'Capucino', 3.99, 'Coffee');
-- INSERT INTO Product VALUES (NULL, 'Espresso', 1.99, 'Coffee');
-- INSERT INTO Product VALUES (NULL, 'Latte', 2.99, 'Coffee');
-- INSERT INTO Product VALUES (NULL, 'Water', 1.99, 'NoCoffee');
-- INSERT INTO Product VALUES (NULL, 'Chai', 1.99, 'NoCoffee');
-- INSERT INTO Product VALUES (NULL, 'Mocha', 4.99, 'Coffee');

-- CREATE TABLE Customer (
--     CustomerId INTEGER PRIMARY KEY, 
--     CustomerName VARCHAR(256) NOT NULL, 
--     CustomerEmail VARCHAR(256) UNIQUE,
--     CustomerRegistrationDate DATE
-- );

-- INSERT INTO Customer VALUES (NULL, 'Bob', 'bob@gmail.com', DATE('now'));
-- INSERT INTO Customer VALUES (NULL, 'Jeb', 'jeb@gmail.com', DATE('now'));
-- INSERT INTO Customer VALUES (NULL, 'Tom', 'tom@gmail.com', DATE('now'));

-- CREATE TABLE "Order" (
--     OrderId INTEGER PRIMARY KEY, 
--     OrderDatetime DATETIME,
--     CustomerId INTEGER, 
--     ProductId INTEGER,
--     FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
--     FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
-- );

-- PRAGMA foreign_keys = true;

-- INSERT INTO "Order" VALUES (NULL, DATETIME('now'), 95, 1);

DELETE FROM Product WHERE ProductId = 1;
