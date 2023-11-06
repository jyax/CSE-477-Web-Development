CREATE TABLE IF NOT EXISTS `experiences` (
`exp_id`            int(11)         NOT NULL AUTO_INCREMENT     COMMENT 'The experience ID',
`pos_id`            int(11)         NOT NULL                    COMMENT 'FK:The Position ID reference',
`name`              varchar(100)    NOT NULL                    COMMENT 'Name of the experience',
`description`       TEXT            NOT NULL                COMMENT 'Description of the experience',
`hyperlink`         TEXT            DEFAULT NULL                COMMENT 'URL to learn more about the experience',
`start_date`        DATE            DEFAULT NULL                COMMENT 'Start date of the experience',
`end_date`          DATE            DEFAULT NULL                COMMENT 'End date of the experience',
PRIMARY KEY (`exp_id`),
FOREIGN KEY (pos_id) REFERENCES positions(pos_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Experiences I have had at a given position';