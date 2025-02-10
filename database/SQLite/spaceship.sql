CREATE TABLE Astronauts (
  id integer primary key,
  name text,
  role text,
  missions integer
);

INSERT INTO Astronauts VALUES (null, 'Dr. Berhe', 'Engineer',0);
INSERT INTO Astronauts VALUES (NULL, 'Ekam', 'Engineer',0);
INSERT INTO Astronauts VALUES (NULL, 'Matthew <3', 'Commander', 0);
INSERT INTO Astronauts VALUES (NULL, 'Shoji', 'Scientist', 0);
INSERT INTO Astronauts VALUES (NULL, 'Winstar', 'Scientist',0);
INSERT INTO Astronauts VALUES (NULL, 'Michael', 'Engineer',4);
INSERT INTO Astronauts VALUES (NULL, 'Russell', 'Engineer', 0);
INSERT INTO Astronauts VALUES (NULL, 'Estevahn', 'Engineer', 5);
INSERT INTO Astronauts VALUES (NULL, 'Vong', 'Engineer', 3);
INSERT INTO Astronauts VALUES (NULL, 'David', 'Scientist',0);
INSERT INTO Astronauts VALUES (NULL, 'Dr. Ayhan', 'Engineer',1907);
INSERT INTO Astronauts VALUES (NULL, 'Jonathan', 'Scientist', 2);
INSERT INTO Astronauts VALUES (NULL, 'Tristan', 'Engineer',9);
INSERT INTO Astronauts VALUES (NULL, 'Dr. Ripley', 'Scientist',20);
INSERT INTO Astronauts VALUES (NULL, 'Fernando', 'Engineer',17);
INSERT INTO Astronauts VALUES (NULL,'Parneet', 'Scientist',  4);

-- SELECT * FROM Astronauts;

CREATE TABLE Missions (
  id integer primary key,
  name text,
  destination text,
  crew integer,
  status text
);

INSERT INTO Missions VALUES (NULL, 'Mission Difficult','Planet Far Away', 4, 'Ongoing');
INSERT INTO Missions VALUES (NULL, 'Mission Difficult','uranus', 4000000000, 'Completed');
INSERT INTO Missions VALUES (NULL, 'Mission Easy', 'Jupiter',  4, 'Completed');
INSERT INTO Missions VALUES (NULL, 'Mission Impossible','Planet Saturn', 3, 'Ongoing');
INSERT INTO Missions VALUES (NULL, 'Mission 0', 'Neptune', 5, 'Completed');
INSERT INTO Missions VALUES (NULL, 'Death Star Recon', '6th Star Cluster', 3, 'Completed');
INSERT INTO Missions VALUES (NULL, 'Flora Collection', 'P4-20',6, 'Planned');
INSERT INTO Missions VALUES (NULL, 'Mission Extremely Difficult','Planet Area 51', 3, 'Completed');
INSERT INTO Missions VALUES (NULL, 'Save Matthew <3','Unknown', 1, 'Planned');
INSERT INTO Missions VALUES (NULL, 'Mission 0', 'Jupiter', 2, 'Ongoing');
INSERT INTO Missions VALUES (NULL, 'Don't Starve','Stranded', 15, 'Ongoing');
INSERT INTO Missions VALUES (NULL, 'Easy','Beteigeuze', 4, 'Completed');

-- SELECT * FROM Missions;

CREATE TABLE Spaceship (
  id integer primary key,
  name text,
  shiptype text,
  fuelLevel integer
);

-- Shuttle, Rover, Mothership
INSERT INTO Spaceship VALUES (NULL, 'DHL ship','Rover', 47);
INSERT INTO Spaceship VALUES (NULL, 'Good ship','Shuttle', 4);
INSERT INTO Spaceship VALUES (NULL, 'abandoned ship','Mothershp', 0);
INSERT INTO Spaceship VALUES (NULL, 'WALL-E','Rover', 10);
INSERT INTO Spaceship VALUES (NULL, 'UPS','Mothership', 3);
INSERT INTO Spaceship VALUES (NULL, 'Slave 1','Rover', 2);
INSERT INTO Spaceship VALUES (NULL, 'USS SULACO','Mothership', 10);
INSERT INTO Spaceship VALUES (NULL, 'Apollo 23', 'Shuttle', 80);
INSERT INTO Spaceship VALUES (NULL, 'Galaxy Doo Ship', 'Rover', 7) ;
INSERT INTO Spaceship VALUES (NULL, 'Starship Enterprise', 'Mothership', 9) ;

-- SELECT * FROM Spaceship;

CREATE TABLE AlienEncounters (
  id integer primary key,
  missionId integer,
  species text,
  communication text,
  foreign key (missionId) references Missions(id)
);

-- Friendly, Hostile, Neutral
INSERT INTO AlienEncounters VALUES (NULL, 2, 'Teraner', 'Neutral');
INSERT INTO AlienEncounters VALUES (NULL, 2, 'Homer simpson', 'Neutral');
INSERT INTO AlienEncounters VALUES (NULL, 2, 'Enderman', 'Neutral');
INSERT INTO AlienEncounters VALUES (NULL, 9, 'Spring', 'Friendly');
INSERT INTO AlienEncounters VALUES (NULL, 7, 'Tyrinid','Hostile');
INSERT INTO AlienEncounters VALUES (NULL, 1, 'Freakazoid', 'Hostile');
INSERT INTO AlienEncounters VALUES (NULL, 5, 'Pretzel', 'Hostile');

-- SELECT * FROM AlienEncounters;

CREATE TABLE Score (
  id integer primary key,
  team text,
  score integer
);

INSERT INTO Score VALUES (NULL, 'a team', 0);
INSERT INTO Score VALUES (NULL, 'b Team', 0);
INSERT INTO Score VALUES (NULL, 'Gold Team', 0);
INSERT INTO Score VALUES (NULL, 'Cardboard Addiction', 0);
INSERT INTO Score VALUES (NULL, 'DBMS', 0);
INSERT INTO Score VALUES (NULL, 'PH Team', 0);
INSERT INTO Score VALUES (NULL, 'Game Addicts', 0);
INSERT INTO Score VALUES (NULL, 'Sleeper Agent', 0);
INSERT INTO Score VALUES (NULL, 'Solo Squads', 0);
INSERT INTO Score VALUES (NULL, 'Avengers', 1);
INSERT INTO Score VALUES (NULL, 'Rebel Alliance', 0);
INSERT INTO Score VALUES (NULL, 'Ultramarines', 0);

SELECT COUNT(*) FROM Astronauts; -- team “b team”
SELECT COUNT(*) FROM Astronauts; -- Rebel Alliance
SELECT COUNT(*) FROM Astronauts; --PH team

update Score SET Score = Score + 1 where team = 'b team' or team = 'Rebel Alliance' or team = 'PH team';    

-- SELECT Count(*) FROM Missions WHERE status = 'Planned';  
-- SELECT (*) FROM Missions WHERE status = “Planned”;  – b Team
-- SELECT (*) FROM Missions WHERE status = “Planned” ;-- GameAddicts
-- SELECT FROM Missions WHERE status = “Planned”;- - Cardboard Addiction
SELECT * FROM Missions WHERE status = 'Planned'; -- Avengers

update Score SET Score = Score + 1 where team = 'Avengers';    

SELECT * FROM Score;
