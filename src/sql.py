"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1111',
                             db='wyydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# 根据用户id获取其排行的音乐id
def get_music(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT `music_id` FROM `musics` WHERE user_id=%s ORDER BY music_id"
        cursor.execute(sql, user_id)
        return cursor.fetchall()


# 根据用户id获取歌词
def get_lyric(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT `lyric` FROM `lyrics`,`musics` WHERE lyrics.`music_id`=musics.`music_id` AND musics.`user_id`=%s"
        cursor.execute(sql, user_id)
        return cursor.fetchall()


# 根据用户id获取歌手
def get_artist(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT `nickname` FROM `musics` WHERE user_id=%s"
        cursor.execute(sql, user_id)
        return cursor.fetchall()


# 保存歌词
def insert_lyric(music_id, lyric):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `lyrics` (`music_id`, `lyric`) VALUES (%s, %s)"
        cursor.execute(sql, (music_id, lyric))
    connection.commit()


# 保存音乐
def insert_music(user_id, music_id, music_name, nickname):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `musics` (`user_id`,`music_id`, `music_name`, `nickname`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, music_id, music_name, nickname))
    connection.commit()


# 获取所有音乐的 ID\歌词\歌手
def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `music_id` FROM `musics` ORDER BY music_id"
        cursor.execute(sql, ())
        return cursor.fetchall()


def get_all_lyric():
    with connection.cursor() as cursor:
        sql = "SELECT `lyric` FROM `lyrics`  "
        cursor.execute(sql, ())
        return cursor.fetchall()


def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `nickname` FROM `musics`  "
        cursor.execute(sql, ())
        return cursor.fetchall()


def less_than_one(user_id):
    with connection.cursor() as cursor:
        sql = "call proc (%s)"
        cursor.execute(sql, user_id)
        return cursor.fetchall()


def dis_connect():
    connection.close()


# 清库
def truncate_all():
    with connection.cursor() as cursor:
        sql = "truncate table musics"
        cursor.execute(sql, ())
        sql = "truncate table lyrics"
        cursor.execute(sql, ())
    connection.commit()
