# ----------------用户注册页验证器----------------------
# ---------------------------------------------------

from werkzeug.security import check_password_hash
from wtforms import StringField, IntegerField, Form, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Email, ValidationError
from flask_login import login_user

from app.models.user import User


class LoginFrom(Form):
    email = StringField(
        validators=[DataRequired(), Length(min=8, max=64),
                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(
        validators=[DataRequired(message='密码不可以为空，请输入密码'), Length(6, 32)])

    def check_password(self):
        user = User.query.filter_by(email=self.data['email']).first()
        if user:
            if check_password_hash(user.password, self.password.data):
                # 把用户登录成功的凭证放入到Cookies中
                # remember=True 默认cookies过期时间为关闭当前浏览器就销毁, remember=True就一直有效 时长为365天 一个自然年
                login_user(user, remember=True)
                return True
        return False
