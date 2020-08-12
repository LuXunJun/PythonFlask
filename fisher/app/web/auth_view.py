from flask_login import logout_user

from . import web
from flask import render_template, request, redirect, url_for, flash

from app.forms.register import RegisterFrom
from app.models.base import db
from app.models.user import User
from app.forms.login import LoginFrom


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            # user.password(form.password)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom(request.form)
    if request.method == 'POST':
        # 判断用户登录请求
        if form.check_password():
            flash('登录成功！')
        else:
            flash('登录失败！')
        # 重定向页面地址
        next = request.args.get('next')
        if not next or not next.startswith('/'):
            next = url_for('web.index')
        return redirect(next)

    return render_template('auth/login.html', form={'data':{'email': 'demo@demo.iu'}})



@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
