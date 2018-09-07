CREATE DATABASE gas_measurements;
USE gas_measurements;
CREATE USER gas_recorder IDENTIFIED BY 'strawberry';
GRANT ALL ON gas_measurements TO gas_recorder;

CREATE TABLE measurements(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor VARCHAR(8),
    reading FLOAT,
    ro FLOAT NULL,
    temperature FLOAT NULL,
    rel_humidity FLOAT NULL,
    upload_ts TIMESTAMP NULL
);

CREATE TABLE ros(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor VARCHAR(8),
    ro FLOAT
);