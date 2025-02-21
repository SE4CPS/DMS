DROP TABLE IF EXISTS mission CASCADE;
DROP TABLE IF EXISTS spaceship CASCADE;
DROP TABLE IF EXISTS encounter CASCADE;

CREATE TABLE IF NOT EXISTS spaceship (
    identifier SERIAL PRIMARY KEY,
    spaceship_name VARCHAR(256),
    spaceship_type VARCHAR(256),
    spaceship_fuel_level INTEGER CHECK (spaceship_fuel_level >= 0)
);

CREATE TABLE IF NOT EXISTS encounter (
    identifier SERIAL PRIMARY KEY,
    encounter_species VARCHAR(256),
    threat_level VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS mission (
    identifier SERIAL PRIMARY KEY,
    role_name VARCHAR(256) NOT NULL DEFAULT 'Astronaut',
    description TEXT,
    planet VARCHAR(256),
    crew_size INTEGER CHECK (crew_size > 0),
    status VARCHAR(256) NOT NULL DEFAULT 'STANDBY' CHECK (status IN ('STANDBY', 'PROGRESS', 'COMPLETED')),
    team VARCHAR(256),
    experience INTEGER,
    spaceship_id INTEGER,
    encounter_id INTEGER,
    FOREIGN KEY (spaceship_id) REFERENCES spaceship(identifier),
    FOREIGN KEY (encounter_id) REFERENCES encounter(identifier)
);

INSERT INTO spaceship (spaceship_name, spaceship_type, spaceship_fuel_level) VALUES
('Apollo 23', 'Shuttle', 80),
('Andromeda Explorer', 'Shuttle', 85),
('SL 1', 'Rover', 2),
('Abandoned ship', 'Mothership', 0);

INSERT INTO encounter (encounter_species, threat_level) VALUES
('Enderman', 'Hostile'),
('Pretzel', 'Hostile'),
('Tyrinid', 'Hostile');

INSERT INTO mission (role_name, experience, description, planet, crew_size, status, 
                     team, spaceship_id, encounter_id)
VALUES
('Engineer', 0, 'Mission Extremely Difficult', 'Planet Area 51', 3, 'COMPLETED', 
 'Gold Team', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Apollo 23'),
 (SELECT identifier FROM encounter WHERE encounter_species = 'Enderman')),

('Scientist', 17, 'Flora Collection', 'P4-20', 6, 'STANDBY', 
 'B Team', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Andromeda Explorer'),
 (SELECT identifier FROM encounter WHERE encounter_species = 'Pretzel')),

('Engineer', 2, 'Flora Collection', 'P4-20', 6, 'STANDBY', 
 'B Team', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Andromeda Explorer'),
 (SELECT identifier FROM encounter WHERE encounter_species = 'Tyrinid')),

('Engineer', 0, 'Mission Extremely Difficult', 'Planet Area 51', 3, 'COMPLETED', 
 'Rebel Alliance', (SELECT identifier FROM spaceship WHERE spaceship_name = 'SL 1'),
 NULL),

('Commander', 0, 'Mission Extremely Difficult', 'Planet Area 51', 3, 'COMPLETED', 
 'Avengers', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Abandoned ship'),
 NULL),

('Scientist', 20, 'Mission Extremely Difficult', 'Planet Area 51', 3, 'COMPLETED', 
 'Avengers', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Abandoned ship'),
 NULL),

('Engineer', 5, 'Mission Extremely Difficult', 'Planet Area 51', 3, 'COMPLETED', 
 'Avengers', (SELECT identifier FROM spaceship WHERE spaceship_name = 'Abandoned ship'),
 NULL);

SELECT m.description AS mission, COUNT(e.encounter_species) AS hostile_count
FROM mission m
INNER JOIN encounter e ON m.encounter_id = e.identifier
WHERE e.threat_level = 'Hostile'
GROUP BY m.description
HAVING COUNT(e.encounter_species) > 1
ORDER BY hostile_count DESC
LIMIT 5;
