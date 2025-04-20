-- -- Create data
-- CREATE TABLE team2_flowers (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     last_watered DATE NOT NULL,
--     water_level INT NOT NULL,
--     min_water_required INT NOT NULL
-- );
-- -- Insert data
-- INSERT INTO team2_flowers (name, last_watered, water_level, min_water_required) 
-- VALUES 
-- ('Rose', '2025-03-10', 20, 5),
-- ('Tulip', '2025-03-08', 10, 7),
-- ('Lily', '2025-03-05', 3, 5),
-- ('Lavender', '2025-03-09', 10, 7),
-- ('Hydrangea','2025-03-08', 15, 12),
-- ('Anemone', '2025-03-07', 12, 8);

-- Update
ALTER TABLE team2_flowers
ADD COLUMN max_water_required INT NOT NULL DEFAULT 30;

-- Customers
CREATE TABLE team2_customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Orders
CREATE TABLE team2_orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES team2_customers(id),
    flower_id INT REFERENCES team2_flowers(id),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE
);