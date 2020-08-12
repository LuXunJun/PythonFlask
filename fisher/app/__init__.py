from flask import Flask
from app.models.base import db
from flask_login import LoginManager

# 定义使用login_manager 一定要去实现 @login_manager.user_loader，不然代码会报错
login_manager = LoginManager()

def create_app():
    """
    创建app(flask核心对象)对象
    :return:app
    """
    app = Flask(__name__)

    # 加载配置文件，配置文件在当前目录下config.py
    # 注意：app.config['DEBUG']其中的 DEBUG 必须为大写，因为from_object这种形式加载config必须名称为大写，不然会自己过滤掉
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    # 将sqlalchemy db的对象和app进行挂钩 sqlalchemy db -> app
    # 读取建立数据库连接
    db.init_app(app)
    # 用户登录空间
    login_manager.init_app(app)
    # 如果页面需要登录后访问，那么没有登录的情况下 自动跳转到 endpint = web.register 注册页面
    login_manager.login_view = "web.login"
    # 跳转到注册页提示的Flash 闪现消息指定
    login_manager.login_message = "请先登录！"
    # create_all创建数据模型 到mysql
    db.create_all(app=app)
    return app


def register_blueprint(app):
    """
    将蓝图挂钩到app(flask核心对象)对象中
    :param app: flask核心内容
    :return: 无
    """
    from app.web import web
    app.register_blueprint(web)
