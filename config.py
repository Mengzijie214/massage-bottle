import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_CURSORCLASS = 'DictCursor'
    WTF_CSRF_ENABLED = True

# print("验证环境变量：")
# print("MYSQL_USER ->",os.getenv('MYSQL_USER'))
# print("MYSQL_DB ->",os.getenv('MYSQL_DB'))
#
# # 测试输出
# if __name__ == '__main__':
#     print('当前数据库用户：', Config.MYSQL_HOST)