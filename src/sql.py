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



    
def get_lyr():
    with connection.cursor() as cursor:
        sql = "SELECT `lyric` FROM `lyrics`  "
        cursor.execute(sql, ())
        return cursor.fetchall()

def get_artist():
    with connection.cursor() as cursor:
        sql = "SELECT nickname FROM `musics`  "
        cursor.execute(sql, ())
        return cursor.fetchall()

# 保存歌词
def insert_lyric(music_id, lyric):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `lyrics` (`music_id`, `lyric`) VALUES (%s, %s)"
        cursor.execute(sql, (music_id, lyric))
    connection.commit()

# 保存音乐
def insert_music(music_id, music_name, nickname):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `musics` (`music_id`, `music_name`, `nickname`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (music_id, music_name, nickname))
    connection.commit()

# 获取所有音乐的 ID

def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `music_id` FROM `musics` ORDER BY music_id"
        cursor.execute(sql, ())
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
