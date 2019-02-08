
DROP TABLE IF EXISTS `global_constants`;
CREATE TABLE `global_constants` (
  `key` VARCHAR(64) NOT NULL,
  `value` VARCHAR(128) NOT NULL,
  `lastUpdateDateTime` DATETIME NOT NULL,
  PRIMARY KEY (`key`));

