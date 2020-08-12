from flask import Flask, current_app
from werkzeug.local import Local
import threading

app = Flask(__name__)

app.config.from_object('app.secure')

# -----------------------------------------------Flask核心对象------------------------------------------------
"""
    注意点：
    1、 在离线应用（不是通过web请求的形式）或 单元测试 必须将app_context上下文推入到  _app_ctx_stack栈,
        不然flask不会自己推入，也意味着current_app的代理函数为空
    2、 如果是是一个web请求的话,flask或构建Request及RequestContext,在将RequestContext推入到_requet_ctx_stack
        之前，会去判断_app_ctx_stack栈中的内容是否为空或者不是最新的上下文,如果为None,Flask流程如下：
                    {
        web请求开始->     1）app_context     -Push-> _app_ctx_stack(栈)
                         2) RequestContext -Push-> _requet_ctx_stack(栈)
                    }
                    
                    {
        web请求结束<-     1）app_context     <-Pop- _app_ctx_stack(栈)
                         2) RequestContext <-Pop- _requet_ctx_stack(栈)
                    }
              
    3、 如果_app_ctx_stack与_requet_ctx_stack 栈中的数据都为None的话,那么 current_app 和 request 本地代理的值都为None
        他们只会获取【栈】中的top(1)的数据、流程如下：
        {
            1、current_app -> _app_ctx_stack -> Top1的[app_context]上下文对象中[app](Flask核心对象数据)
            2、request     -> _requet_ctx_stack -> Top1的[RequestContext]上下文对象中[Request](发起当前请求的内容，URL与传递的参数)
        }
"""
# 获取Flask的上下文
ctx = app.app_context()
# 将Flask上下文 push -> _app_ctx_stack栈
ctx.push()
print(f'数据库配置连接地址:{current_app.config["SQLALCHEMY_DATABASE_URI"]}')
# 将Flask上下 _app_ctx_stack栈 -> pop
ctx.pop()

# 通过with 的 __enter__ 和 __exit__ 自动调用 push 和 pop
with app.app_context() as ctx:
    print(f'ctx:{ctx}')
    print(f'[with]数据库配置连接地址:{current_app.config["SQLALCHEMY_DATABASE_URI"]}')


# ----------------------------------------------with-------------------------------------------------

class withDemo:

    def __enter__(self):
        print('打开数据连接')
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """
        :param exc_type: 错误类型
        :param exc_value: 错误值
        :param tb: 错误堆栈信息
        :return: { 1、False | 2、 True}  1、False：外部 Exception 对象接受并处理错误 2、True: __exit__函数体内处理错误
        """
        if tb:
            print('有异常')
        else:
            print('没有异常')

        print('关闭数据连接')
        # return { 1、False | 2、 True}
        # False：外部 Exception 对象接受并处理错误
        # True: __exit__函数体内处理错误
        return True

    def querydemo(self):
        print('查询字段')


"""
    with代码的执行流程 流程图如下：
    {
        1、【with withDemo() as w】 ->  【def __enter__(self) 中的 return self ->  w 对象】
        2、【w.querydemo()】        ->  【def querydemo(self)】
        3、【def __exit__(self, exc_type, exc_value, tb)】
    }
    
"""
try:
    with withDemo() as w:
        1 / 0
        w.querydemo()
except Exception as e:
    print(f'外部接受到的异常:{e}')

# ---------------------------------------------contextlib-------------------------------------------------
from contextlib import contextmanager


# 简化了with代码流程，无需写__enter__和__exit__的方法
# 使用与带非自己写的类的流程包装
class ContextmanagerDemo:

    def querydemo(self):
        print('contextmanager 查询字段')


# 一、具有返回对象的形式
#   定义流程代码
@contextmanager
def make_contextmanagerdemo():
    print('contextmanager 打开数据连接')
    yield ContextmanagerDemo()
    print('contextmanager 关闭数据连接')


# 使用方式
with make_contextmanagerdemo() as r:
    r.querydemo()


# 二、当前对象形式
# 业务基类泛指平时我们使用的第三方库中的操作基类

# 基类
class ContextmanagerDemoBase2:
    def __init__(self):
        pass

    def querydemo(self):
        print('contextmanagerBase2 查询字段')


# 派生类对基类扩展
class ContextmanagerDemo2(ContextmanagerDemoBase2):
    @contextmanager
    def make_ContextmanagerDemo2(self):
        try:
            print('----------------------------------')
            print('contextmanager2 打开数据连接')
            yield
            print('contextmanager2 提交操作')
            print('contextmanager2 关闭数据连接')
            print('----------------------------------')
        except Exception as e:
            print('contextmanager2 回滚数据rollback')
            print('----------------------------------')
            raise e


# 声明对象
cmanager = ContextmanagerDemo2()

# 使用封装的方法 包括 调用基类的方法 和 派生类的方法
with cmanager.make_ContextmanagerDemo2():
    print('业务类开始')
    cmanager.querydemo()
    print('业务类结束')

# -----------------------------------------------线程隔离------------------------------------------------

# Local为线程隔离对象，每一个线程里面的值都是独立的，不会在多线程中被篡改
# Local的实现原理使用的是Python的字典 {进程id:对象}
# ident = self.__ident_func__() 获取线程id
my_obj = Local()
my_obj.b = 1


def worker():
    my_obj.b = 2
    # 新线程
    print(f'in new thread b is {my_obj.b}')


t1 = threading.Thread(target=worker)
t1.start()
t1.join()
# 主线程
print(f'in main thread b is {my_obj.b}')


# -----------------------------------------------可调用对象------------------------------------------------
# 可调用对象最大的特征 对象名称 可以像 方法一样使用，关键是一定要实现__call__的方法

class objectdemo():

    # 初始化函数
    def __init__(self):
        pass

    # 可调用对象必须实现__call__的方法
    def __call__(self, context):
        print('--------------------------------------------------')
        print(f'数据为:{context}')
        print('数据为:' + context)
        print('数据为:{0}'.format(context))
        print('数据为:{data}'.format(data=context))


obj = objectdemo()
obj('Hello 、Python')


# -----------------------------------------------**kwargs的理解------------------------------------------------
# 1、字符型、数值型、单个对象、对象列表都可以通过kwargs来获取使用

def kwargsmethod(**kwargs):
    print('--------------------------------------------------')
    print(kwargs['name'])  # 字符型
    print(kwargs['age'])  # 数值型
    print(kwargs['person'].name)  # 单个对象
    print(kwargs['perpons'] if len(kwargs['perpons']) > 0 else None)  # 对象列表


class perpon:
    def __init__(self, name, age):
        self.name = name
        self.age = age


perpons = []
p = perpon('李四_单', 20)
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for num in range(1, 10):
    perpons.append(perpon('李四_集' + str(num + 1), 20))

kwargsmethod(name='zhangsan', age=19, person=p, nums=nums, perpons=perpons)

# -----------------------------------------------生成用户令牌----------------------------------------------------
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 安全密钥key
secret_key = '/a/b/c/d/e/f'
value = 'userid'
expiration = 600


def generate_token(value):
    s = Serializer(secret_key, expiration)
    token = s.dumps({'id': value}).decode('utf-8')
    return token


def decode_token(token):
    s = Serializer(secret_key, expiration)
    t = token.encode('utf-8')
    data = s.loads(t)
    return data.get('id')


token = generate_token(value)
result = decode_token(token)
print('--------------------------------------------------')
print(f'1、加密后的数据:{token}')
print(f'2、解密后的数据:{result}')
print('--------------------------------------------------')


# -----------------------------------------------对象赋值 浅copy----------------------------------------------------

# 浅copy: 会为每个对象开辟新的内存空间, 但只会做类结构中的第一层数据的copy，对于嵌套数据 如：列表，自定义类型 都只会引用之前对象
# 深copy: 会为每个对象开辟新的内存空间, 对于第一层数据和嵌套数据都会copy出一整套数据

class base:
    # 动态赋值 浅copy代码
    def setattr(self, dict_attr):
        for key, value in dict_attr.items():
            if hasattr(self, key):
                setattr(self, key, value)


class a(base):
    id = 0
    name = ''
    a1 = None

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.a1 = a1(2, '李四')


class b(base):
    id = 0
    name = ''
    a1 = None


class a1:
    aid = 0
    aname = ''

    def __init__(self, id, name):
        self.aid = id
        self.aname = name


a = a(1, '张三')

b = b()

# 动态赋值 浅copy
b.setattr(a.__dict__)

print(id(a))

print(id(b))

print('--------------------------------------------------')
print(f'a_id:{a.id}[{id(a.id)}] a_name:{a.name}[{id(a.name)} ] a_object:{a.a1.aname} [{id(a.a1.aname)}]')
print(f'b_id:{b.id}[{id(b.id)}] b_name:{b.name}[{id(b.name)}] b_object:{b.a1.aname}[{id(b.a1.aname)}]')
print('--------------------------------------------------')
a.id = 3
a.name = 'lxj'
a.a1.aname = '王五'
print(f'a_id:{a.id}[{id(a.id)}] a_name:{a.name}[{id(a.name)} ] a_object:{a.a1.aname} [{id(a.a1.aname)}]')
print(f'b_id:{b.id}[{id(b.id)}] b_name:{b.name}[{id(b.name)}] b_object:{b.a1.aname}[{id(b.a1.aname)}]')
print('--------------------------------------------------')

import copy

l1 = [1, 2, 3, 4, 5, [22, 33]]
#l2 = l1.copy()
l2 = copy.deepcopy(l1)
l1[0] = 0
l1[-1].append(44)
print((l1))
print((l2))