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
