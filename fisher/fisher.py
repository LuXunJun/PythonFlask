# --------------目录---------------
# 1、创建app对象并挂钩blueprint蓝图对象，最终blueprint对象里添加的路由信息，
#    都会合并到app对象中的url_map 和 view_function中，endpoint= 蓝图名称(web).视图函数名(search)
# 2、启动服务进程开启服务
# --------------------------------
from app import create_app

# 获取封装的app对象
app = create_app()

if __name__ == '__main__':
    # debug=True 开启debug模式 修改代码后 无需反复重启服务器
    # app.config['DEBUG']读取config文件下的DEBUG字段
    app.run(host='127.0.0.1', debug=app.config['DEBUG'], port=81)
