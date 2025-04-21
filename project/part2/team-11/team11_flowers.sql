CREATE TABLE team11_flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    last_watered TEXT NOT NULL,
    water_level INTEGER NOT NULL,
    min_water_required INTEGER NOT NULL
);

CREATE TABLE team11_customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE team11_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT REFERENCES team11_customers(id),
    flower_id INT REFERENCES team11_flowers(id),
    order_date DATE NOT NULL
);

CREATE INDEX IF NOT EXISTS index_orders_customer_id ON team11_orders(customer_id);
CREATE INDEX IF NOT EXISTS index_orders_flower_id ON team11_orders(flower_id);
CREATE INDEX IF NOT EXISTS index_customer_id ON team11_customers(id);
CREATE INDEX IF NOT EXISTS index_flowers_id ON team11_flowers(id);

/*
INSERT INTO team11_flowers (name, last_watered, water_level, min_water_required) 
VALUES 
('Rose', '2024-02-10', 20, 5),
('Tulip', '2024-02-08', 10, 7),
('Lily', '2024-02-05', 3, 5);
*/