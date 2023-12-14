CREATE TABLE IF NOT EXISTS `scores` (
`score_id`      int(11)         NOT NULL auto_increment     COMMENT 'the id of the score',
`score`         int(11)         DEFAULT NULL                COMMENT 'the score the user got',
`username`      varchar(100)    NOT NULL                    COMMENT 'the users username',
PRIMARY KEY (`score_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='The user scores for wordly';