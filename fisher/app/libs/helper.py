
class Helper:
    def __init__(self, word):
        self.word = word

    def is_isbn_or_key(self):
        """
        用于判断使用的isbn还是word_key
        :return: 返回判定它执行返回的类型
        """
        isbn_or_key = 'key'
        if len(self.word) == 13 and self.word.isdigit():
            isbn_or_key = 'isbn'
        short_word = self.word.replace('-', '')
        if '-' in self.word and len(short_word) == 10 and short_word.isdigit():
            isbn_or_key = 'isbn'
        return isbn_or_key
