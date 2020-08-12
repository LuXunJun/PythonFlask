
from flask import current_app, flash, render_template

from . import web
from flask_login import login_required, current_user

from app.libs.helper import Helper
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.service.yushu_book import YuShuBook


@web.route('/my/gifts')
@login_required
def my_gifts():
    return "my gifts"


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    gift = Gift()
    # 1、判断书籍是否在书籍库中(api)中真实存在
    # 2、一个用户不能同时存在赠送者和索要者
    # 3、此用户即不在礼物清单、也心愿清单才能添加
    if is_book_by_isbn(isbn):
            # and not is_gift_user(isbn) and not is_wish_user(isbn):
        with db.auto_commit():
            gift.isbn = isbn
            gift.uid = current_user.id
            # current_user.bean += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        # 闪现消息
        flash('这本书不存在或者已经添加到你的礼物清单与心愿清单了，不能重复添加！')
    # return render_template("book_detail.html", book=bookview, wishes=[], gifts=[])

@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass


def is_book_by_isbn(isbn):
    # 校验此isbn在书籍库(api)中是否存在
    helper = Helper(isbn)
    if helper.is_isbn_or_key() == 'isbn':
        yushu = YuShuBook()
        yushu.search_by_isbn(isbn)
        return yushu.first
    return False

def is_gift_user(isbn):
    return Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first


def is_wish_user(isbn):
    return Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first

# 这样写不好，不够抽象，而且只能当前视图使用
# @contextmanager
# def make_db():
#     try:
#         yield db
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e






