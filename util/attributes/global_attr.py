# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : global_attr.py
@Author   :wangmaosheng
@Date     : 2025/2/16 17:47
@Desc:    : 获取全球商品分类
"""
import time

import requests

from global_data import global_obj
from tokens.get_token import get_current_user_token
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_global_attributes():
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    app_key = global_obj.production_conf['tk_util']['app_key']
    token = get_current_user_token()
    headers = {
        "x-tts-access-token": token,
        "content-type": "application/json"
    }
    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_categories?category_version=v1&timestamp={timestamp}&app_key={app_key}&locale=zh-CN"
    request = requests.Request(method="GET", url=url, headers=headers)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.get(url_finally, headers=headers)
    return response.text
