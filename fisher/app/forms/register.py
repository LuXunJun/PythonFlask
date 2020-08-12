# ----------------用户注册页验证器----------------------
# ---------------------------------------------------
from wtforms import StringField, IntegerField, Form, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Email, ValidationError

from app.models.user import User


class RegisterFrom(Form):
    nickname = StringField(
        validators=[DataRequired(),
                    Length(min=2, max=10, message='昵称至少需要两个字符，最多10个字符')])
    email = StringField(
        validators=[DataRequired(), Length(min=8, max=64),
                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(
        validators=[DataRequired(message='密码不可以为空，请输入密码'), Length(6, 32)])

    # 自定义校验器 _email _后面的字段会去对应 上面声明的email
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            # 这里使用raise 抛出去的错误会被模板的 form.errors 进行处理
            raise ValidationError('电子邮件已经被注册！')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称不能重复！')