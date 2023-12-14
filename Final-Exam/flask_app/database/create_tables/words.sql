CREATE TABLE IF NOT EXISTS `words` (
`word_id`      int(11)          NOT NULL auto_increment     COMMENT 'the id of the word of the day',
`date`         datetime         DEFAULT NULL                COMMENT 'the date of the word',
`word`      varchar(16)         NOT NULL                    COMMENT 'the word of the day',
PRIMARY KEY (`word_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='The word of the day  for wordly';