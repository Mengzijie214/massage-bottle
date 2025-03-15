# 应用初始化
import os

from flask import Flask
from .extensions import mysql
# from dotenv import load_dotenv
# load_dotenv()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mysql.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

# class Config:
#     MYSQL_USER = os.getenv('MYSQL_USER')
#     MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')