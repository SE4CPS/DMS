CREATE TABLE team7_flowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_watered DATE NOT NULL,
    water_level INT NOT NULL,
    min_water_required INT NOT NULL
);

INSERT INTO team7_flowers (name, last_watered, water_level, min_water_required) 
VALUES 
('Rose', '2024-02-10', 20, 5),
('Tulip', '2024-02-08', 10, 7),
('Lily', '2024-02-05', 3, 5);