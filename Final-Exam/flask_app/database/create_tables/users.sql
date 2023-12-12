CREATE TABLE IF NOT EXISTS `users` (
`email`     varchar(255)    NOT NULL        COMMENT 'email of the user',
`password`  varchar(255)    NOT NULL        COMMENT 'encrypted password',
`role`      varchar(16)     DEFAULT 'user'  COMMENT 'Role of the user',
PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User login information';