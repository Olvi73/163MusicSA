-- 歌词表
CREATE TABLE `lyrics` (
  `music_id` BIGINT(20) NOT NULL,
  `lyric` TEXT DEFAULT NULL,
  PRIMARY KEY (`music_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4;

-- 歌曲表
CREATE TABLE `musics` (
  `music_id` INT(20) NOT NULL,
  `music_name` VARCHAR(255) DEFAULT NULL,
  `nickname` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`music_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4;