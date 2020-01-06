# 初始化app
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from app.models.base import db
from flask_cors import *


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    # 注册蓝图
    register_blueprint(app)
    # 注册SQLAlchemy
    db.init_app(app)
    # with app.app_context()
    db.create_all(app=app)
    # 注册logger
    register_logger(app=app)
    # 解决跨域
    CORS(app, supports_credentials=True)

    return app


# 注册蓝图
def register_blueprint(app):
    # 注册book里web的蓝图
    from app.web import web
    app.register_blueprint(web)


def register_logger(app):
    handler = RotatingFileHandler(app.config['LOG_FILE_PATH'], maxBytes=1024 * 1024, backupCount=5)
    # fmt = '%(asctime)s - %(filename)s:%(lineno)s - func: [%(name)s] - %(message)s'
    fmt1 = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt1)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
