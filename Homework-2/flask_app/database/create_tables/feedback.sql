CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`    int(11)         NOT NULL AUTO_INCREMENT         COMMENT 'Comment ID',
`name`          varchar(100)    NOT NULL                        COMMENT 'Name of the commentator',
`email`         varchar(255)    DEFAULT NULL                     COMMENT 'Email of the commentator',
`comment`       text            DEFAULT NULL                    COMMENT 'Text of the comment',
PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Feedback I have received';