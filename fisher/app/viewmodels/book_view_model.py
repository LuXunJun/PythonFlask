from app.service.yushu_book import YuShuBook


class Book:
    def __init__(self, book):
        self.title = book['title']
        self.author = '、'.join(book['author'])
        self.binding = book['binding']
        self.category = book['category']
        self.image = book['image']
        self.pages = book['pages']
        self.price = book['price']
        self.pubdate = book['pubdate']
        self.publisher = book['publisher']
        self.summary = book['summary']
        self.isbn = book['isbn']
        # self.intro = self.builderintro()

    # 使用property包装体，就可以在外围的时候使用book.intro属性的形式了
    @property
    def intro(self):
        return ' | '.join(filter(lambda x: True if x else False, [self.author, self.publisher, self.price]))

    @classmethod
    def get_book_byisbn(cls, isbn):
        yushu = YuShuBook()
        yushu.search_by_isbn(isbn)
        return yushu.first

class BookView:
    def __init__(self):
        self.keyword = ''
        self.books = []
        self.total = 0

    def fill(self, key, YuShuBook):
        self.keyword = key
        self.total = YuShuBook.total
        self.books = [Book(book) for book in YuShuBook.books]
