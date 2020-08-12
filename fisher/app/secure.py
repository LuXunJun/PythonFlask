# --------------目录---------------
# 用于对加密信息的保存，例如：数据库账户、
# --------------------------------

DEBUG = True
# cymysql 连接mysql的驱动程序
# SQLALCHEMY_DATABASE_URI必须为这个名称
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123123@localhost:3306/fisher'
SECRET_KEY = '112233/112233'
