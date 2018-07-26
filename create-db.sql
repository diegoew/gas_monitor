CREATE DATABASE gas_measurements;
USE gas_measurements;
CREATE USER gas_recorder@localhost IDENTIFIED BY 'strawberry';
GRANT ALL ON gas_measurements TO gas_recorder@localhost;

CREATE TABLE measurements(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor VARCHAR(8),
    reading FLOAT,
    ro FLOAT NULL,
    upload_ts TIMESTAMP NULL
);
