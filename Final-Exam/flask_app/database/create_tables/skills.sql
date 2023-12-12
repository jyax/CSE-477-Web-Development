CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`          int(11)             NOT NULL AUTO_INCREMENT     COMMENT 'Skill ID',
`exp_id`            int(11)             NOT NULL                    COMMENT 'Experience ID reference',
`name`              varchar(100)        NOT NULL                    COMMENT 'Name of the skill',
`skill_level`       int                 DEFAULT NULL                COMMENT 'level of skill, 1 to 10',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (exp_id) REFERENCES experiences(exp_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT = 'Skills I have obtained from experiences';