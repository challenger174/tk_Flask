# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_product_attributes.py
@Author   :wangmaosheng
@Date     : 2025/2/5 00:58
@Desc:    : 商品的属性信息，填的补充程度高的情况会提升曝光
"""
import json
import logging
import time

import requests
from openai import OpenAI

from global_data import global_obj
from tokens.get_token import get_current_user_token
from update_data_to_tk.util.create_request_body import get_global_categories
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_global_attribute():
    """
    获取属性相关的信息
    :return: 一个字典类型的数据
    """
    attr_arr = []
    attrs = global_obj.production_conf['attributes']['attrs']
    for attr in attrs:
        if int(attr['type_id']) != 0:
            dict_attr = {
                "id": str(attr['id']),
                "values": [
                    {"id": str(attr["type_id"]),
                     "name": str(attr["type_name"])
                     }
                ]
            }
        else:
            dict_attr = {
                "id": str(attr['id']),
                "values": [
                    {
                     "name": str(attr["type_name"])
                     }
                ]
            }
        attr_arr.append(dict_attr)
    return attr_arr
    # attr_arr = []
    # category_id = get_global_categories(title)
    # app_secret = global_obj.global_config['tk_util']['app_secret']
    # app_key = global_obj.global_config['tk_util']['app_key']
    # timestamp = int(time.time())
    # url = f'https://open-api.tiktokglobalshop.com/product/202309/categories/{category_id}/global_attributes?timestamp={timestamp}&app_key={app_key}&locale=zh-CN&category_version=v1'
    # token = get_current_user_token()
    # headers = {
    #      "x-tts-access-token": token,
    #      "content-type": "application/json"
    # }
    # request = requests.Request(method="GET", url=url, headers=headers)
    # sign = generate_signature(request, app_secret)
    # url_finally = url + f'&sign={sign}'
    # response = requests.get(url_finally, headers=headers)
    # resonse_json = response.json()
    # logging.info(f"response_json: {response.text}")
    # if response.status_code == 200:
    #     # attributes = resonse_json['data']['attributes']
    #     client = OpenAI(api_key=global_obj.gpt_conf['attribute_category_gpt']['api'],
    #                     base_url=global_obj.gpt_conf['attribute_category_gpt']['base_url'])
    #
    #     system_role = global_obj.gpt_conf['attribute_category_gpt']['system_role']
    #     if attr is not None:
    #         response = client.chat.completions.create(
    #             model=global_obj.gpt_conf['attribute_category_gpt']['gpt_module'],
    #             messages=[
    #                 {"role": "system", "content": system_role},
    #                 {"role": "user", "content": f"message: {title} {attr} role: {response.text}"
    #                 }
    #             ],
    #             stream=False,
    #             temperature=0.7
    #         )
    #     else:
    #         response = client.chat.completions.create(
    #             model=global_obj.gpt_conf['attribute_category_gpt']['gpt_module'],
    #             messages=[
    #                 {"role": "system", "content": system_role},
    #                 {"role": "user", "content": f"message: {title} role: {response.text}"
    #                  }
    #             ],
    #             stream=False,
    #             temperature=0.7)
    #     res_data = response.choices[0].message.content
    #     logging.info(f"商品信息 {res_data}")
    #     if response.choices[0].finish_reason == 'stop':
    #         return response.choices[0]
    #     else:
    #         return None
    # else:
    #     return None



