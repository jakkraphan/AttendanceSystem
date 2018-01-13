CREATE TABLE IF NOT EXISTS `department`(
   `d_id` INT  NOT NULL AUTO_INCREMENT,
   `d_name` VARCHAR(50) NOT NULL,
   `d_info` TEXT,
   PRIMARY KEY ( `d_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user`(
   `user_id` INT NOT NULL AUTO_INCREMENT,
   `d_id` INT ,
   `password` VARCHAR(30) NOT NULL,
   `name` VARCHAR(30) NOT NULL,
   `info` TEXT,
    PRIMARY KEY ( `user_id` ),
    FOREIGN KEY (`d_id`) REFERENCES `department`(`d_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- CREATE TABLE IF NOT EXISTS `employee`(
--    `user_id` INT NOT NULL,
--     `d_id` INT NOT NULL,
--     PRIMARY KEY ( `user_id` ),
--     FOREIGN KEY (`d_id`) REFERENCES `department`(`d_id`),
--     FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `manage`(
   `user_id` INT,
   `d_id` INT,
   PRIMARY KEY ( `user_id` ),
   FOREIGN KEY (`d_id`) REFERENCES `department`(`d_id`),
   FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- CREATE TABLE IF NOT EXISTS `personal_manager`(
--    `user_id` INT,
--    PRIMARY KEY ( `user_id` )
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- CREATE TABLE IF NOT EXISTS `system_manager`(
--    `user_id` INT,
--    PRIMARY KEY ( `user_id` )
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE IF NOT EXISTS `attendance_table`(
   `user_id` INT,
   `m_date` DATE,
   `check_in_time` TIME,
   `check_out_time` TIME,
   `status` INT,
   PRIMARY KEY ( `user_id` ,`m_date`),
   FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `leave_table`(
   `number` INT AUTO_INCREMENT,
   `user_id` INT,
   `begin_time` DATE,
   `end_time` DATE,
   `reason` TEXT,
   `reply` TEXT,
   `m_type` INT,
   `status` INT,
   PRIMARY KEY ( `number` ),
   FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `trip_table`(
   `number` INT AUTO_INCREMENT,
   `user_id` INT,
   `begin_time` DATE,
   `end_time` DATE,
   `reason` TEXT,
   `reply` TEXT,
   `m_type` INT,
   `status` INT,
   PRIMARY KEY ( `number` ),
   FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `log`(
   `user_id` INT,
   `info` TEXT,
   `l_time` TIMESTAMP DEFAULT current_timestamp,
   PRIMARY KEY ( `user_id`,`l_time`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `check_time`(
   `c_date` DATE,
   `check_in_time` TIME,
   `check_out_time` TIME,
   PRIMARY KEY ( `c_date`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

