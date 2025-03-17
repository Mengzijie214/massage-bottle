# 数据库模型
from functools import wraps

from app.extensions import mysql
from passlib.hash import sha256_crypt

# 用户表查询
class User:
    @staticmethod
    def create(username, password):
        cursor = mysql.connection.cursor()
        hashed_pw = sha256_crypt.hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)',
                      (username, hashed_pw))
        mysql.connection.commit()
        return cursor.lastrowid

# 漂流瓶表查询
class Bottle:
    @staticmethod
    def create(user_id, content):
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO bottles (user_id, content) VALUES (%s, %s)',
                      (user_id, content))
        mysql.connection.commit()
        return cursor.lastrowid

# 链接表
class Reply:
    @staticmethod
    def create(bottle_id, user_id, content):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO replies (bottle_id, user_id, content)
            VALUES (%s, %s, %s)
        ''', (bottle_id, user_id, content))
        mysql.connection.commit()
        return cursor.lastrowid