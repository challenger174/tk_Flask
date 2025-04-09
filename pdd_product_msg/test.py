# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : test.py
@Author   :wangmaosheng
@Date     : 2025/2/11 23:09
@Desc:    :
"""

import requests


if __name__ == '__main__':
    url = "https://mobile.yangkeduo.com/goods.html?ps=eeRAraD11Y"
    response = requests.get(url=url)
    print(response.text)