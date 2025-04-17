CREATE TABLE team7_orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES team7_customers(id),
    flower_id INT REFERENCES team7_flowers(id),
    order_date DATE
);

INSERT INTO team7_orders ()
VALUES
