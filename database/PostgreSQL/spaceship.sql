CREATE TABLE IF NOT EXISTS Astronauts (
  id SERIAL PRIMARY KEY,
  name TEXT,
  role TEXT,
  missions INTEGER
);

INSERT INTO Astronauts (name, role, missions) VALUES
('Dr. Berhe', 'Engineer', 0),
('Ekam', 'Engineer', 0),
('Matthew <3', 'Commander', 0),
('Shoji', 'Scientist', 0),
('Winstar', 'Scientist', 0),
('Michael', 'Engineer', 4),
('Russell', 'Engineer', 0),
('Estevahn', 'Engineer', 5),
('Vong', 'Engineer', 3),
('David', 'Scientist', 0),
('Dr. Ayhan', 'Engineer', 1907),
('Jonathan', 'Scientist', 2),
('Tristan', 'Engineer', 9),
('Dr. Ripley', 'Scientist', 20),
('Fernando', 'Engineer', 17),
('Parneet', 'Scientist', 4);

CREATE TABLE IF NOT EXISTS Missions (
  id SERIAL PRIMARY KEY,
  name TEXT,
  destination TEXT,
  crew INTEGER,
  status TEXT
);

INSERT INTO Missions (name, destination, crew, status) VALUES
('Mission Difficult', 'Planet Far Away', 4, 'Ongoing'),
('Mission Difficult', 'Uranus', 40000, 'Completed'),
('Mission Easy', 'Jupiter', 4, 'Completed'),
('Mission Impossible', 'Planet Saturn', 3, 'Ongoing'),
('Mission 0', 'Neptune', 5, 'Completed'),
('Death Star Recon', '6th Star Cluster', 3, 'Completed'),
('Flora Collection', 'P4-20', 6, 'Planned'),
('Mission Extremely Difficult', 'Planet Area 51', 3, 'Completed'),
('Save Matthew <3', 'Unknown', 1, 'Planned'),
('Mission 0', 'Jupiter', 2, 'Ongoing'),
('Dont Starve', 'Stranded', 15, 'Ongoing'),
('Easy', 'Beteigeuze', 4, 'Completed');

CREATE TABLE IF NOT EXISTS Spaceship (
  id SERIAL PRIMARY KEY,
  name TEXT,
  shiptype TEXT,
  fuelLevel INTEGER
);

INSERT INTO Spaceship (name, shiptype, fuelLevel) VALUES
('DHL ship', 'Rover', 47),
('Good ship', 'Shuttle', 4),
('Abandoned ship', 'Mothership', 0),
('WALL-E', 'Rover', 10),
('UPS', 'Mothership', 3),
('Slave 1', 'Rover', 2),
('USS SULACO', 'Mothership', 10),
('Apollo 23', 'Shuttle', 80),
('Galaxy Doo Ship', 'Rover', 7),
('Andromeda Explorer', 'Shuttle', 85),
('Starship Enterprise', 'Mothership', 9);

CREATE TABLE IF NOT EXISTS AlienEncounters (
  id SERIAL PRIMARY KEY,
  missionId INTEGER REFERENCES Missions(id),
  species TEXT,
  communication TEXT
);

INSERT INTO AlienEncounters (missionId, species, communication) VALUES
(2, 'Teraner', 'Neutral'),
(2, 'Homer Simpson', 'Neutral'),
(2, 'Enderman', 'Neutral'),
(9, 'Spring', 'Friendly'),
(7, 'Tyrinid', 'Hostile'),
(1, 'Freakazoid', 'Hostile'),
(5, 'Pretzel', 'Hostile');

CREATE TABLE IF NOT EXISTS Score (
  id SERIAL PRIMARY KEY,
  team TEXT,
  score INTEGER DEFAULT 0
);

INSERT INTO Score (team, score) VALUES
('A Team', 0),
('B Team', 0),
('Gold Team', 0),
('Cardboard Addiction', 0),
('DBMS', 0),
('PH Team', 0),
('Game Addicts', 0),
('Sleeper Agent', 0),
('Solo Squads', 0),
('Avengers', 1),
('Rebel Alliance', 0),
('Ultramarines', 0);

UPDATE Score SET score = score + 1 WHERE team IN ('B Team', 'Rebel Alliance', 'PH Team');

SELECT * FROM Missions WHERE status = 'Planned'; -- Avengers

UPDATE Score SET score = score + 1 WHERE team = 'Avengers';

SELECT * FROM Score;
