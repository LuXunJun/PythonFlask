from app.libs.httper import HTTP
# ---------获取当前上下文中的app对象(flask核心对象)---------------
from flask import current_app
# -----------------------------------------------------------

# 构建面向对象的类、需要体现类的 类据性、类特征
class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = 'http://t.talelin.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.books = []
        self.total = 0

    # 查询单本书籍
    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        book = HTTP.get(url)
        self.books = [book]
        self.total = 1

    # 查询多本书籍
    def serach_by_keyword(self, keyword, page):
        url = self.keyword_url.format(keyword, current_app.config['PRE_PAGE'], self.calculate_start(page))
        books = HTTP.get(url)
        self.books = books['books']
        self.total = books['total']

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PRE_PAGE']

    @property
    def first(self):
        return self.books[0] if len(self.books) >= 1 else None

class _YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def serach_by_keyword(cls, keyword, page):
        url = cls.keyword_url.format(keyword, current_app.config['PRE_PAGE'], cls.calculate_start(page))
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PRE_PAGE']



