-- Drop table if exists (for re-running the script)
DROP TABLE IF EXISTS Flowers;

-- Create the Flowers table
CREATE TABLE Flowers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    color VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    blooming_season VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial sample data
INSERT INTO Flowers (name, scientific_name, color, price, stock_quantity, blooming_season)
VALUES 
    ('Rose', 'Rosa', 'Red', 2.50, 100, 'Spring'),
    ('Tulip', 'Tulipa', 'Yellow', 1.80, 150, 'Spring'),
    ('Sunflower', 'Helianthus', 'Yellow', 3.00, 75, 'Summer'),
    ('Orchid', 'Orchidaceae', 'Purple', 5.50, 50, 'All Year'),
    ('Lily', 'Lilium', 'White', 2.20, 80, 'Summer');

-- Generate 100,000 rows efficiently using CROSS JOIN
INSERT INTO Flowers (name, scientific_name, color, price, stock_quantity, blooming_season)
SELECT 
    f.name, f.scientific_name, f.color, f.price, f.stock_quantity, f.blooming_season
FROM Flowers f
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) a
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) b
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) c
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) d
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) e
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) f
LIMIT 99995;  -- Ensuring total row count reaches 100,000

-- Verify row count
SELECT COUNT(*) AS total_rows FROM Flowers;

-- Measure Query Performance BEFORE Index
SET @start = (SELECT NOW(3));
SELECT * FROM Flowers WHERE color = 'Red' LIMIT 10;
SET @end = (SELECT NOW(3));
SELECT 'Execution Time BEFORE Index' AS profile_stage, TIMESTAMPDIFF(MICROSECOND, @start, @end) / 1000 AS execution_time_ms;

-- Add an Index
CREATE INDEX idx_color ON Flowers(color);

-- Measure Query Performance AFTER Index
SET @start = (SELECT NOW(3));
SELECT * FROM Flowers WHERE color = 'Red' LIMIT 10;
SET @end = (SELECT NOW(3));
SELECT 'Execution Time AFTER Index' AS profile_stage, TIMESTAMPDIFF(MICROSECOND, @start, @end) / 1000 AS execution_time_ms;
