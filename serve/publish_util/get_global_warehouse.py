# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_global_warehouse.py
@Author   :wangmaosheng
@Date     : 2025/2/15 10:49
@Desc:    : 获取全球仓库列表信息，咋发布的时候会使用到
"""
import logging
import sys
import time

import requests

from global_data import global_obj
from tokens.get_token import get_current_user_token
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_global_warehouse():
    """
    后去全球商品的仓库地理位置
    :return:
    """
    # 获取当前用户的唯一标识,唯一标识，表示是给哪个店铺上品的，和mysql的tk_user_token_msg自增id对齐
    token = get_current_user_token()
    # 符合预期的情况下
    app_key = global_obj.production_conf['tk_util']['app_key']
    app_secret = global_obj.production_conf['tk_util']['app_secret']

    return get_autorized_shop(token, app_key, app_secret)

    # headers = {
    #     'x-tts-access-token': token,
    #     'content-type': 'application/json'
    # }
    # timestamp = int(time.time())
    # url = f"https://open-api.tiktokglobalshop.com/logistics/202309/warehouses?timestamp={timestamp}&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&app_key=29a39d"


def get_autorized_shop(token, app_key, app_secret):
    """
    获取店铺的授权信息
    :return:
    """
    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/authorization/202309/shops?app_key={app_key}&timestamp={timestamp}"
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }
    request = requests.Request(method="GET", url=url, headers=headers)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    logging.info(f"sign计算成功，进行数据请求rul: {url_finally}")
    response = requests.get(url_finally, headers=headers)
    print(response.text)
    if response.status_code == 200 and response.json()['message'].lower() == 'success':
        print(response.json()['data'])
        return response.text
    else:
        logging.error("请求商家信息失败")

