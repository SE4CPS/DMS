CREATE TABLE IF NOT EXISTS Bikes (
      bike_id SERIAL PRIMARY KEY,
      brand VARCHAR(50),
      encrypted_price BYTEA,
      color VARCHAR(30)
  );
  
   CREATE TABLE IF NOT EXISTS Sales (
      sale_id SERIAL PRIMARY KEY,
      bike_id INT,
      sale_date DATE,
      sale_price DECIMAL(10, 2),
      FOREIGN KEY (bike_id) REFERENCES Bikes(bike_id)
  );  
  
-- ALTER TABLE Bikes ALTER COLUMN brand TYPE TEXT;
  
-- CREATE INDEX brandIdx on Bikes(brand);
 CREATE EXTENSION IF NOT EXISTS pgcrypto;
    
-- INSERT INTO Sales (bike_id, sale_date, sale_price) VALUES (934, '2025-04-04', 999.99);
  
-- DELETE FROM Bikes;
 
-- INSERT into Bikes (brand, encrypted_price, color) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut vehicula tortor, sit amet sagittis nunc. Aenean lobortis diam quis dolor ultricies, ac lacinia lectus ultrices. Integer sagittis mauris at fringilla efficitur. Curabitur porta gravida leo, non congue elit fringilla non. Nunc et erat porta, egestas odio eu, pretium orci. Ut vestibulum magna nec finibus mattis. Nulla gravida dolor lobortis purus iaculis fermentum. Aliquam vel magna eu erat fermentum aliquet eget nec leo. Donec rhoncus metus et est placerat aliquet et a erat. Donec ut elementum ligula. Nullam interdum dolor eu elementum tempus. Nullam elit dui, molestie in congue id, hendrerit tempor lectus. Etiam tempus leo id elit volutpat vulputate. Nulla justo augue, volutpat ut erat non, tincidunt tincidunt neque. Quisque sodales sollicitudin massa molestie euismod. Nam velit sapien, maximus id bibendum in, condimentum lacinia libero.Pellentesque sed convallis nisi. Suspendisse elementum turpis eget bibendum vehicula. Mauris elit justo, lobortis et mauris vel, ornare ornare elit. In tristique leo at lectus mattis, ut aliquet elit ultrices. Sed leo augue, pellentesque semper mauris non, vulputate iaculis metus. Ut feugiat nulla suscipit orci imperdiet vulputate. Ut in arcu urna. Quisque faucibus faucibus odio, ac tincidunt augue molestie at. Quisque consectetur id lectus sed dictum. Aliquam eu nisl ornare sapien consequat aliquet ut at est. Sed vulputate efficitur nulla ac semper. Quisque in enim sollicitudin, aliquet nulla ac, suscipit odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.Maecenas accumsan varius lorem ut blandit. Maecenas id rhoncus lorem. Donec dolor purus, bibendum vestibulum laoreet non, rhoncus ut augue. Phasellus cursus elementum leo vel pellentesque. Proin interdum mauris quis turpis euismod, sed pulvinar neque porttitor. Duis sit amet auctor nisl. Proin ullamcorper auctor suscipit. Sed pretium nibh eu magna faucibus gravida. Nunc vitae ipsum ex. Aenean vel maximus diam. Mauris venenatis ex a nibh gravida, sed egestas lacus mattis.Suspendisse congue venenatis malesuada. Donec consequat enim sit amet dui maximus aliquet. Sed elementum consectetur nulla. Nam non fermentum ipsum, non ultrices urna. Sed posuere aliquet ex, vel congue sem pharetra ut. Etiam leo nibh, ornare et sagittis et, lacinia a nisl. Duis in est nisl. Sed pharetra vulputate quam vel mattis. Etiam a dictum libero. Aliquam a ullamcorper enim, sed tempus lorem. Morbi sodales purus quam, nec sodales lectus pellentesque et. Nam tortor sem, fringilla sit amet sodales vel, pretium non est. Proin dignissim sit amet tortor vitae euismod. Etiam a nunc pretium, feugiat nisi quis, finibus quam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;Fusce et mauris et orci condimentum condimentum eget at odio. Etiam accumsan ligula et neque hendrerit, auctor volutpat dolor ultrices. Maecenas et nisl blandit, tincidunt ipsum ac, ullamcorper lacus. Proin et sagittis lectus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Etiam convallis hendrerit turpis, a tincidunt lacus rutrum vitae. Donec vestibulum orci ex, ut sagittis orci tristique sodales. Sed non quam placerat, euismod augue non, volutpat dui. In maximus diam non tortor ullamcorper hendrerit.', pgp_sym_encrypt('999.99', 'my_strong_password'), 'orange');

-- EXPLAIN ANALYZE UPDATE Bikes SET brand = 'SCHWINN'; 
-- EXPLAIN ANALYZE SELECT FROM Bikes WHERE color = 'orange'; 
-- EXPLAIN ANALYZE SELECT brand, pgp_sym_decrypt(encrypted_price, 'my_strong_password') FROM Bikes ORDER BY Brand;

EXPLAIN ANALYZE SELECT bike_id FROM Bikes;
