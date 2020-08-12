# ------------------------------------------------
# 使用wtforms用于请求参数的验证
# ------------------------------------------------

from wtforms import IntegerField, StringField, Form
from wtforms.validators import Length, NumberRange, DataRequired

# 测试信息
# 测试Windows
class SearchForm(Form):
    # 这里的名称必须和url地址上的参数名称一致，区分大小写
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
