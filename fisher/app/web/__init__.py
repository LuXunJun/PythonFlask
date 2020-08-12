# 蓝图用于分割多个业务层 一个app对象 -> 多个蓝图对象
from flask import Blueprint, render_template

web = Blueprint('web', __name__)


# 404 处理程序
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import auth_view
from app.web import book_view
from app.web import drift_view
from app.web import gift_view
from app.web import main_view
from app.web import wish_view
