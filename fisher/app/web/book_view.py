from flask import jsonify, request, json, render_template, flash

from . import web
from app.libs.helper import Helper
from app.service.yushu_book import YuShuBook
from app.viewmodels.book_view_model import BookView, Book
from app.forms.book import SearchForm


@web.route('/hello')
def hello():
    return 'hello flask'


@web.route('/JinjaDemo')
def JinjaDemo():
    data = [{'name': 'JinjaDemo', 'text': 'this is JinjaDemo'}
        , {'name': 'JinjaDemo2', 'text': 'this is JinjaDemo2'}
        , {'name': 'JinjaDemo3', 'text': 'this is JinjaDemo3'}]
    return render_template('JinjaDemo.html', data=data)


# 也是可以通过add_url_rule的方法来实现路由的注册
# app.add_url_rule('/hello/',view_func=hello)


@web.route('/book/search')
def search():
    # 判断使用的ibsn还是word_key
    # isbn_or_key = is_isbn_or_key(q)
    # ---------使用 if else 非三元的方式实现------------
    # if isbn_or_key == 'isbn':
    #     return YuShuBook.search_by_isbn(q)
    # else:
    #     return YuShuBook.serach_by_keyword(q)
    # -----------------------------------------------

    # -----------使用python自带的json实现返回json格式与定义header头上的content-type的内容------------------------------
    # return json.dumps(YuShuBook.search_by_isbn(q) if isbn_or_key == 'isbn' else YuShuBook.serach_by_keyword(q)) \
    #     , 200, {'content-type': 'application/json'}
    # ----------------------------------------------------------------------------------------------------------

    # -------------flask框架中的jsonify实现对json的封装、包括 header 头上的指定 'content-type': 'application/json' 与状态码的定义

    # ------------页面验证器--------------
    form = SearchForm(request.args)
    # ----------------------------------
    # if form.validate():
    #     q = form.q.data.strip()
    #     page = form.page.data
    #     isbn_or_key = is_isbn_or_key(q)
    #     return jsonify(YuShuBook.search_by_isbn(q) if isbn_or_key == 'isbn' else YuShuBook.serach_by_keyword(q,page))
    # return jsonify({'Message': '找不到当前数据'}), 404
    # ----------------------------------------------------------------------------------------------------------
    bookbusiness = YuShuBook()
    bookview = BookView()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        helper = Helper(q)
        isbn_or_key = helper.is_isbn_or_key()
        if isbn_or_key == 'isbn':
            bookbusiness.search_by_isbn(q)
        else:
            bookbusiness.serach_by_keyword(q, page)
        bookview.fill(q, bookbusiness)
        # ----------------------------------------------------------
        # default=lambda o: o.__dict__ 是解决复杂对象序列化问题、
        # 当在对象中有自定义对象的时候json.dumps提供default来处理dumps无法处理的序列化
        # 因为要转换成json 1）源数据 -转换成-> dict 2) json.dumps -转换成-> json格式
        # bookview -|
        #            key:String
        #            total:Int
        #            books:List[Book] <- bookview.__dict__ 将无法序列化成字典,此时 需要需要手动将Book对象转换成字典,这个时候就会去执行default函数了
        # ----------------------------------------------------------
        print(f'dict{bookview.__dict__}')
        # return json.dumps(bookview.__dict__, default=lambda o: o.__dict__), {'content-type': 'application/json'}
    else:
        # return jsonify({'Message': '找不到当前数据'}), 404
        flash('找不到当前数据')

    return render_template("search_result.html", books=bookview)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    bookbusiness = YuShuBook()
    bookbusiness.search_by_isbn(isbn)
    bookview = Book(bookbusiness.first)
    return render_template("book_detail.html", book=bookview, wishes=[], gifts=[])

