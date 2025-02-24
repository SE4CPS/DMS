-- Drop and recreate Flowers table
DROP TABLE IF EXISTS Flowers;
CREATE TABLE Flowers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    color VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    blooming_season VARCHAR(50)
);

-- Insert sample data
INSERT INTO Flowers (name, scientific_name, color, price, stock_quantity, blooming_season)
VALUES 
    ('Rose', 'Rosa', 'Red', 2.50, 100, 'Spring'),
    ('Tulip', 'Tulipa', 'Yellow', 1.80, 150, 'Spring'),
    ('Sunflower', 'Helianthus', 'Yellow', 3.00, 75, 'Summer'),
    ('Orchid', 'Orchidaceae', 'Purple', 5.50, 50, 'All Year'),
    ('Lily', 'Lilium', 'White', 2.20, 80, 'Summer');

-- Generate 100,000 rows efficiently
INSERT INTO Flowers (name, scientific_name, color, price, stock_quantity, blooming_season)
SELECT f.name, f.scientific_name, f.color, f.price, f.stock_quantity, f.blooming_season
FROM Flowers f
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) a
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) b
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) c
LIMIT 99995;

-- Measure Query Performance BEFORE Index
SET @start = NOW(3);
SELECT COUNT(*) FROM Flowers WHERE color = 'Red';
SET @end = NOW(3);
SELECT 'BEFORE INDEX' AS stage, TIMESTAMPDIFF(MICROSECOND, @start, @end) / 1000 AS ms;

-- Add an Index
CREATE INDEX idx_color ON Flowers(color);

-- Measure Query Performance AFTER Index
SET @start = NOW(3);
SELECT COUNT(*) FROM Flowers WHERE color = 'Red';
SET @end = NOW(3);
SELECT 'AFTER INDEX' AS stage, TIMESTAMPDIFF(MICROSECOND, @start, @end) / 1000 AS ms;
