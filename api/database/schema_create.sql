CREATE DATABASE  IF NOT EXISTS `protectplayanow2` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `protectplayanow2`;

DROP TABLE IF EXISTS `reading`;
CREATE TABLE `reading` (
  `instant` datetime NOT NULL,
  `deviceId` varchar(36) NOT NULL,
  `gasName` varchar(100) NOT NULL,
  `reading` double NOT NULL,
  `unitOfReading` varchar(100) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `sensorType` varchar(100) NOT NULL DEFAULT '',
  `ro` double DEFAULT NULL,
  `relHumidity` double DEFAULT NULL,
  `tempInCelsius` double DEFAULT NULL,
  `input` double DEFAULT NULL,
  `resolution` double DEFAULT NULL,
  PRIMARY KEY (`instant`,`deviceId`,`gasName`,`sensorType`),
  KEY `sensorTypeIndex` (`sensorType`),
  KEY `indx_instant_gas_deviceId` (`instant`,`deviceId`,`gasName`),
  KEY `inx_deviceId` (`deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;