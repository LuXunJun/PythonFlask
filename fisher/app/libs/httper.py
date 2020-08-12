# urllib   使用起来非常的不智能，使用起来繁琐
# requests 使用起来简单，代码简练，功能强大
# ----------------目录----------------
# 发送http请求
# -----------------------------------

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        """
        用于发送请求
        :param url: 发送API的请求地址
        :param return_json: 是否已JSON格式返回
        :return: 返回API执行后结果
        """
        r = requests.get(url)
        # result
        # 返回的是json格式的数据
        # 将数据转换成json
        # 状态码为非200的状态
        if r.status_code != 200:
            return {} if return_json else ""
        return r.json() if return_json else r.text()
