from flask import render_template

from . import web

from app.models.gift import Gift
from app.viewmodels.book_view_model import Book


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [Book(Book.get_book_byisbn(gift.isbn)) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
