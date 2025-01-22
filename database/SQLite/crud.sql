
-- Use or create the database 'books'
ATTACH DATABASE 'books.db' AS books;

-- Create Library table in 'books' database
CREATE TABLE IF NOT EXISTS books.Library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);

-- Create Book table in 'books' database
CREATE TABLE IF NOT EXISTS books.Book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    library_id INTEGER,
    FOREIGN KEY (library_id) REFERENCES books.Library (id)
);

-- Insert sample data into Library
INSERT INTO books.Library (name, location) VALUES ('Central Library', 'Main Street');
INSERT INTO books.Library (name, location) VALUES ('West End Library', 'West Avenue');

-- Insert sample data into Book
INSERT INTO books.Book (title, author, library_id) VALUES ('Python Programming', 'John Doe', 1);
INSERT INTO books.Book (title, author, library_id) VALUES ('Data Science Basics', 'Jane Smith', 1);

-- Read data from Library
SELECT * FROM books.Library;

-- Read data from Book
SELECT * FROM books.Book;

-- Update Library data
UPDATE books.Library 
SET name = 'Updated Central Library', location = 'Updated Main Street' 
WHERE id = 1;

-- Update Book data
UPDATE books.Book 
SET title = 'Advanced Python Programming', author = 'John Smith', library_id = 1 
WHERE id = 1;

-- Delete a record from Library
DELETE FROM books.Library WHERE id = 2;

-- Delete a record from Book
DELETE FROM books.Book WHERE id = 2;
