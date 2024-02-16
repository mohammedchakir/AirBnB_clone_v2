-- Task3: Prepare MySQL server for the project
-- Create or update the hbnb_dev user with the specified privileges
-- Create or update the hbnb_dev_db database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Ensure that the hbnb_dev user has privileges only on the specified database
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;