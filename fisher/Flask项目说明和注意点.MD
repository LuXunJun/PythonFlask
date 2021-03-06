

####============== Flask 项目目录结构 ==============

    app-|
        forms-| # 用于对于控件验证的目录
                book.py
                login.py
                register.py
    
        libs-|  # 自定义的一些帮助类与处理类
                __init__.py
                helper.py
                httper.py
    
        models-| # 数据模型类
                base.py
                book.py
                gift.py
                user.py
                wish.py
    
        spider-| # 爬虫类
                __init__.py
                yushu_book.py
    
        static-| # 静态数据
                 # 存放css、js、image
    
        Templates-| # 模板文件
                    # Jinja2引擎前端页面
    
        viewmodels-| # 视图模型
                     # 前端数据展示模型
    
        web-|  # 用于获取请求的类
                __init__.py #web的初始化文件(blueprint 蓝图)
                book.py
    
        test-| # 单元测试示例代码
               # 代码示例和代码片段.py
    
        __init__.py #app的初始化文件(create_app app文件)
        secure.py  #配置文件：DB用户名密码
        setting.py #配置文件：基本状态，常量数据
    
    fisher.py #启动文件



####============== Flask 核心机制  ==============

###python模块(.py文件)加载流程 ：
     同一个模块（.py文件），在一次执行里面只会导入一次 注意：import 导入只会一次！！！

###Flask机制：

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


####============== Python 多线程说明 ==============

###Python 多线程说明：
    1、Python 不能充分使用到多核的优势
    2、不能使用多核的优势的原因是，CPython的解释器有一个全局的锁(GIL)，相对来说保证线程数据安全性
    3、Python解释器，解释代码是已 byteCode 形式解释 例如：
        a+=1 分为三个byteCode的形式
        1）获取a的数据值
        2）做相加操作
        3）赋值操作到a

        GIL并不能保证，多个线程中a的数据一定是线程安全的，因为GIL的锁只正对的是byteCode，并不是正对整一段代码段的
        解释器在执行多线程过程中，随时可能挂起一个线程做另一个线程的事，例如：
        {
             假设：A和B 线程都对 a = 5 进行操作，往往a结果可能都等于a = 6

                GIL bytecode Lock加锁:
                    A）A线程获取a变量的数据值 bytecode (A-线程挂起）
                GIL bytecode Lock解锁

                GIL bytecode Lock加锁:
                    B）B线程获取a变量的数据值 bytecode (B-线程调用)
                    B）B线程a变量的数据+1操作 bytecode (B-线程执行)
                    B）B线程a变量的赋值操作 bytecode   (B-线程执行)
                GIL bytecode Lock解锁:

                 GIL bytecode Lock加锁:
                    A）A线程a变量的数据+1操作 bytecode (A-线程恢复）
                    A）A线程a变量的赋值操作 bytecode   (A-线程执行)
                 GIL bytecode Lock解锁:
        }

###Python 多进程和多线程的区别:
    1、多线程：多线程之间内存地址是独立的，资源生成由操作系统分配
    2、多进程：多进程内存中的资源是共享的非独立，我们平时开发多为多线程开发

###Python 线程隔离：
    1、 使用线程隔离的意义在于：是当前线程能正确引用到他自己所创建的对象，而不是引用到其它线程所创建的对象
    2、 Local为线程隔离对象，每一个线程里面的值都是独立的，不会在多线程中被篡改
    3、 Local的实现原理使用的是Python的字典 {线程id:对象}
    4、 ident = self.__ident_func__() 获取线程id
    
#### ============== Flask 异步编程注意 ============== 

    1、在flask异步编程中，需要异步方法中作为参数传递app(Flask核心对象)对象，不能使用current_app进行传递,因为在异步方法中,current_app是
    无法获取到app对象的，原因为：线程隔离对象，无法从隔离栈(localStack)中获取到对象
    2、如果异步方法内需要使用到app对象，在主线程方法中通过 app = current_app._get_current_object() 获取到真正的Flask核心对象，然后
    通过传参形式传入到异步方法内

    current_app = LocalProxy() #线程隔离对象

    例如：
    {
        def 异步方法(app, objects):
            ..........
                app.config['xxx']


        def 主线程方法():
            主线程app = current_app._get_current_object()
            # 开启线程
            t = thread(target=异步方法,args=[主线程app，objects])
            t.start()

    }


### ==============Jinja2 模板引擎 ==============

    Jinja2模板引擎：
    {{ book.summary | default('', true) }} 和 {{ book.summary | default('没有找到') }} 的区别：

        管道判断逻辑 【book.summary】 获取summary是否存在返回为 Ture 和 Flase  -> default('', true)
            如果summary为 Null 或者 None 就显示’‘ 因为default第一个参数为''

        管道判断逻辑 【book.summary】 获取summary是否存在返回为 Ture 和 Flase  -> default('没有找到')
            如果没有summary字段就显示【没有找到】


### ========= request 获取提交值的信息 ==========

    request获取提交值的信息：
    1、当form 指定action的时候 在做submit的时候 method="post" 那么使用request.args.get将无法获取到对应的数据
     <form action="{{ url_for('web.register') }}" method="post">

    2、解决方法 是将 <form action="" ......> action=""的情况下 request.args和 request.form都能获取到数据

    3、request.args : 获取Url上的数据 例如：【http://127.0.0.1:81/register?next=mygiftsre】
                    获取next上的方法为：request.args.get('next')  method = get
    4、request.form : 获取到form表单提交过来的数据 获取form表单的方法为： request.form.get('id')  method = post

    5、redirect(url_for('web.login', next=123)) 生成后的地址为： /login?next=123

### ========= Flask 用户登录模块简 ========= 

  ####Flask用户登录模块简要：
    1、flask_login -> LoginManager[类]：用户登录管理器，最终挂接到app中
    2、flask_login -> login_user[方法]: 将用户信息写入到cookies中，用于整个用户使用周期中被访问、
    3、flask_login -> logout_user[方法]：将用户cookies在浏览器中清除、
    4、flask_login -> login_required[装饰器]：在方法头部引用，用于标注此方法必须登录后才能执行
    5、login_manager-> login_manager.user_loader[装饰器]：从cookies获取用户凭证数据（UID）、用于校验User是否登录合法
        流程：
            1） ->请求到 视图函数头部有 @login_required(必须登录才可以访问函数体内逻辑)
            2） ->通过环绕装饰器 执行头带有 @login_manager.user_loader下的函数
    6、flask_login -> current_user[对象]:验证通过后的用户信息会被保存到current_user上下文对象中去，之后代码中所有用户信息都在此对象中获取

### ======== Flask-SQLAlchemy 查询方式 =========

 ####Flask-SQLAlchemy 查询方式：
     例： Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(30).distinct().all()
     Gift：数据模型类
     filter_by：相当于sql的where
     group_by：分组，这里因为要使用distinct所以必须分组
     order_by：排序，按照时间降序
     desc: 降序方式排列
     limit：相当于sql的top，返回多少行
     distinct：排除重复数据，必须和group_by一起使用，排重的字段按照group_by中指定字段为准
     all:触发执行函数，获取所有行
     first:触发执行函数,只获取第一条数据
     first_or_404: 如果数据为空、就会抛出一个异常

### ========= SQLAlchemy 查询方式 =========

####SQLAlchemy 查询方式：
    例：      db.session.query(Wish).filter(Wish.launched == Flase, Wish.isbn.in_(isbns)).group_by(Wish.isbn).all()
    统计数量   db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == Flase, Wish.isbn.in_(isbns)).group_by(Wish.isbn).all()
    query: 模型实体名称
    filter: 相当于sql的where 表达式
    in_ : in 操作
    all:触发执行函数，获取所有行
    first:触发执行函数,只获取第一条数据
    func.count: 相当于sql的Count
    备注：group_by 和 func.count 联用代码了 分组统计

### ========= 可调用对象 =========

####可调用对象的意义：
    1、简化对象调用的方式，特别在经常使用的对象直接 对象名() 就可以调用，不用去.函数了，简化编码流程
    2、统一调用接口、
    
    例如：
        class a():
            def run():
                return object
    
            def __call__(self):
                return object
    
        class b():
            def go():
                return object
    
            def __call__(self):
                return object
    
        def c():
            return object
    
        # 程序执行入口
        def main(call)
    
            # ----------------------------------- 代码没有统一 --------------------------------------
            # 如果不使用可调用对象，那我们就需要执行下列代码，非常繁琐而且对于流程抽象代码没有办法做成统一
            # 对于call这个参数来说，是无法知道是run()方法还是go()方法的
            # a对象：a.run()
            # b对象：b.go()
            # c函数：c()
    
            # ----------------------------------- 代码统一执行 --------------------------------------
            # 无论在这里你传的是a、b、c 只要使用函数的方法就能够统一执行
            call()
    


####可调用对象的声明：

    Class 可调用对象类():

        # 初始化函数
        def __init__(self):
            pass

        # 可调用对象必须实现__call__的方法
        def __call__(self, context):
            print(f'数据为:{context}')


    可调用对象 = 可调用对象类()
    可调用对象('Hello 、Python')

    -----------输出结果-------------
     'Hello 、Python'

### ========= kwargs的理解 =========

####1、字符型、数值型、单个对象、对象列表都可以通过kwargs来获取使用
    
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