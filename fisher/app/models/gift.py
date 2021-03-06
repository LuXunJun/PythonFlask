from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Gift(BaseModel):
    id = Column(Integer, primary_key=True)
    # 引用User的模型
    user = relationship('User')
    # uid引用的是User下的id 引用user的模型对象
    uid = Column(Integer, ForeignKey('user.id'))
    # isbn
    isbn = Column(String(15), nullable=False)
    # 引用Book的模型
    # book = relationship('Book')
    # uid引用的是Book下的id 引用Book的模型对象
    # bid = Column(Integer, ForeignKey('book.id'))
    # 判定是否已经送出去了
    launched = Column(Boolean, default=False)

    @classmethod
    def recent(cls):
        return Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.id)).limit(30).distinct().all()
