# from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, SmallInteger, Integer


# 在原有的对象中继续封装一层自己的方法
class SubSQLAlchemy(SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            # 生成器
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SubSQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    # create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())

    # 动态赋值方法
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 如果当前对象属性包含attrs_dict中的key的话，就填充self对象类中的属性
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
