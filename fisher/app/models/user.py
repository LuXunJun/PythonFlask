from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash
from app.models.base import BaseModel
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, BaseModel):
    # 这里可以使用__tablename__来指定生成到数据库中的名称，如果不指定数据库表的名称就等于类的名称
    # __tablename__ = 'User1'
    # 用户唯一标识符 主键
    id = Column(Integer, primary_key=True)
    # 昵称
    nickname = Column(String(24), nullable=False)
    # 手机号
    phone_number = Column(String(18), unique=True)
    # 密码
    _password = Column('password', String(128), nullable=False)
    # 邮箱
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    # 积分
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        """
        生成密码属性，用于获取
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
        设置加密密码属性
        :param raw:
        :return:
        """
        self._password = generate_password_hash(raw)


    # 为了使用flask-login插件，必须指定一个被写入到Cookies的数据值
    # def get_id(self):
    #     return self.id


@login_manager.user_loader
# 这样就可以得到用户的模型了,以便使用login_required包装器
# 打上login_manager.user_login装饰器，这样才能被login_manager使用到
# 从Cookies中拿到id号获取用户信息
def get_user(uid):
    return User.query.get(int(uid))
