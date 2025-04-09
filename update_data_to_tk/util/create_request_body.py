# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : create_request_body.py
@Author   :wangmaosheng
@Date     : 2025/2/5 13:31
@Desc:    :
"""
import json
import logging
import time

import requests

from global_data import global_obj
from tokens.get_token import get_current_user_token
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_json(title, description, img_arr, weight, high, width, length, sku):
    """
    :param attr:
    :param title:
    :param description:
    :param img_arr: 描述当中的图片url链接，上传到tk的数据
    :param weight:
    :param high:
    :param width:
    :param length:
    :param sku:
    :return:
    """
    url_arr = [{"uri": item['uri']} for item in img_arr]
    logging.info("请求tk的请求体构建开始： get_json")
    request_body = dict()
    request_body['title'] = title
    request_body['description'] = description
    request_body['category_id'] = str(global_obj.production_conf['attributes']['category_id'])
    request_body['main_images'] = url_arr
    request_body['package_weight'] = {"value": str(weight), "unit": "KILOGRAM"}
    request_body['skus'] = sku
    # request_body['product_attributes'] = attr
    request_body['package_dimensions'] = {
        "length": length,
        "width": width,
        "height": high,
        "unit": "CENTIMETER"
    }
    logging.info(f"字典的结构： {request_body}")
    return request_body


def get_global_categories(title):
    """
    通过标题获取当前货品的分类
    :param title:  翻译之后的英文标题
    :return: 对应的分类
    """
    logging.info("get_global_categories 获取当前货品分类开始")
    app_key = global_obj.global_config['tk_util']['app_key']
    app_secret = global_obj.global_config['tk_util']['app_secret']
    timestamp = int(time.time())
    token = get_current_user_token()
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_categories/recommend?app_key={app_key}&timestamp={timestamp}"
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }
    data = {
        "category_version": "v1",
        "product_title": title
    }
    response = requests.Request(method="POST", url=url, headers=headers, json=data)
    sign = generate_signature(response, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.post(url_finally, headers=headers, json=data)
    logging.info(f"请求分类的时候返回结果：{response.text}")
    detail_json_obj = response.json()
    if response.status_code == 200 and detail_json_obj['message'].lower() == 'success':
        category_id = get_category_id(detail_json_obj['data'])
        logging.info(f"category_id获取成功：{category_id}")
        return category_id
    else:
        logging.error("商品类目获取异常")
        raise ValueError("获取商品类目异常")


def get_category_id(data):
    """
    通过返回的三级类目，进行数据的解析
    :param data: 叶子节点分类ID
    :return: int 叶子节点编号
    """
    return str(data['leaf_category_id'])

