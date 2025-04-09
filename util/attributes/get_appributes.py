# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_appributes.py
@Author   :wangmaosheng
@Date     : 2025/2/5 11:23
@Desc:    :商品信息，单独发送到客户端页面上
"""
import logging
import time

import requests
from openai import OpenAI

from global_data import global_obj
from serve.parse_util.get_product_attributes import get_global_attribute
from tokens.get_token import get_current_user_token
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_attribuets(keyword, parent_id=''):
    """
    关键字
    :param parent_id:
    :param keyword: 通过关键字识别是什么类目，有什么东西
    :return:
    """
    global category_msg
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    app_key = global_obj.production_conf['tk_util']['app_key']
    token = get_current_user_token()
    headers = {
        "x-tts-access-token": token,
        "content-type": "application/json"
    }
    timestamp = int(time.time())
    if parent_id == '':
        category_msg, category_id = get_keyword_category(app_secret, app_key, timestamp, keyword, headers)
        if category_id is None:
            return None
    else:
        category_id = parent_id
    timestamp = int(time.time())
    url = f'https://open-api.tiktokglobalshop.com/product/202309/categories/{category_id}/global_attributes?timestamp={timestamp}&app_key={app_key}&locale=zh-CN&category_version=v1'
    logging.info(f"category_id: {category_id}")
    request = requests.Request(method="GET", url=url, headers=headers)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.get(url_finally, headers=headers)
    logging.info(f"response {response.text}")
    resonse_json = response.text
    print(resonse_json)
    if response.status_code == 200 and parent_id == '':
        return gpt_format(category_msg, resonse_json)
    else:
        # return gpt_format(resonse_json)
        return response.text


def get_keyword_category(app_secret, app_key, timestamp, keyword, headers):
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_categories/recommend?app_key={app_key}&timestamp={timestamp}"
    data = {
        "category_version": "v1",
        "product_title": keyword
    }
    request = requests.Request(method="POST", url=url, headers=headers, json=data)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.post(url_finally, headers=headers, json=data)
    logging.info(f"response {response.text}")
    if response.status_code == 200:
        return response.text, response.json()['data']['leaf_category_id']
    else:
        return None


def gpt_format(category_msg, attr=''):
    """
    attr标签属性
    :param category_msg:
    :param attr:
    :return:
    """
    if attr == '':
        comment = f" category_id: {category_msg}"
    else:
        comment = f" category_id: {category_msg} attr: {attr}"
    client = OpenAI(api_key=global_obj.gpt_conf['attr_show_web']['api'],
                    base_url=global_obj.gpt_conf['attr_show_web']['base_url'])

    system_role = global_obj.gpt_conf['attr_show_web']['system_role']
    response = client.chat.completions.create(
        model=global_obj.gpt_conf['attr_show_web']['gpt_module'],
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": f"{comment}"}

        ],
        stream=False,
        temperature=0.7
    )
    html_content = response.choices[0].message.content
    logging.info(html_content)
    if response.choices[0].finish_reason == 'stop':
        return html_content

