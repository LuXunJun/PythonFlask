from . import web


@web.route('/my/wish')
# @login_required
def my_wish():
    pass


@web.route('/wish/book/<isbn>')
# @login_required
def save_to_wish(isbn):
    pass


@web.route('/satisfy/wish/<int:wid>')
# @login_required
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
# @login_required
def redraw_from_wish(isbn):
    pass
