-- Create data
CREATE TABLE team2_flowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_watered DATE NOT NULL,
    water_level INT NOT NULL,
    min_water_required INT NOT NULL
);
-- Insert data
INSERT INTO team2_flowers (name, last_watered, water_level, min_water_required) 
VALUES 
('Rose', '2025-03-10', 20, 5),
('Tulip', '2025-03-08', 10, 7),
('Lily', '2025-03-05', 3, 5),
('Lavender', '2025-03-09', 10, 7),
('Hydrangea','2025-03-08', 15, 12),
('Anemone', '2025-03-07', 12, 8);
