CREATE TABLE IF NOT EXISTS `users` (
`user_id`   int(11)         NOT NULL auto_increment     COMMENT 'the id of the user',
`username`  varchar(100)    NOT NULL                    COMMENT 'the username of the user',
`email`     varchar(100)    NOT NULL                    COMMENT 'email of the user',
`password`  varchar(256)    NOT NULL                    COMMENT 'encrypted password',
`role`      varchar(10)     NOT NULL                    COMMENT 'Role of the user',
PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='User login information';