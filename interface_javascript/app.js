const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = process.env.PORT || 3000;
const DATABASE = 'bike.db';

app.use(express.static('public'));

// Function to get a database connection
function getDBConnection() {
  return new sqlite3.Database(DATABASE);
}

// Function to initialize the database
function initDB() {
  const bikesToAdd = [
    ['Mountain Bike', 'Off-road'],
    ['Road Bike', 'On-road'],
    ['Hybrid Bike', 'Hybrid'],
    ['BMX', 'Stunt'],
    ['Folding Bike', 'Portable']
  ];

  const db = getDBConnection();
  db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS bikes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      type TEXT NOT NULL
    )`);

    const stmt = db.prepare('INSERT OR IGNORE INTO bikes (name, type) VALUES (?, ?)');
    bikesToAdd.forEach(bike => stmt.run(bike));
    stmt.finalize();
  });
  db.close();
}

// Initialize the database
initDB();

// Middleware to parse JSON requests
app.use(express.json());

// Route to get all bikes
app.get('/bikes', (req, res) => {
  const db = getDBConnection();
  db.all('SELECT * FROM bikes', (err, rows) => {
    if (err) {
      console.error('Error fetching bikes:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json(rows);
    }
  });
  db.close();
});

// Route to add a new bike
app.post('/add_bike', (req, res) => {
  const newBike = req.body;
  const db = getDBConnection();
  db.run('INSERT OR IGNORE INTO bikes (name, type) VALUES (?, ?)', [newBike.name, newBike.type], function(err) {
    if (err) {
      console.error('Error adding bike:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ message: 'Bike added successfully', id: this.lastID });
    }
  });
  db.close();
});

// Route to update a bike
app.put('/update_bike/:id', (req, res) => {
  const { id } = req.params;
  const updateDetails = req.body;
  const db = getDBConnection();
  db.run('UPDATE bikes SET name = ?, type = ? WHERE id = ?', [updateDetails.name, updateDetails.type, id], function(err) {
    if (err) {
      console.error('Error updating bike:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ message: 'Bike updated successfully', changes: this.changes });
    }
  });
  db.close();
});

// Route to delete a bike
app.delete('/delete_bike/:id', (req, res) => {
  const { id } = req.params;
  const db = getDBConnection();
  db.run('DELETE FROM bikes WHERE id = ?', id, function(err) {
    if (err) {
      console.error('Error deleting bike:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ message: 'Bike deleted successfully', changes: this.changes });
    }
  });
  db.close();
});

// Route to delete all bikes
app.delete('/delete_all_bikes', (req, res) => {
  const db = getDBConnection();
  db.run('DELETE FROM bikes', function(err) {
    if (err) {
      console.error('Error deleting all bikes:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ message: 'All bikes deleted successfully', changes: this.changes });
    }
  });
  db.close();
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});