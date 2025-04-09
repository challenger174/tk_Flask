# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : upload_product_to_tk.py
@Author   :wangmaosheng
@Date     : 2025/2/5 13:09
@Desc:    :商品信息上传到tk当中
"""
import logging
import time

import requests

from global_data import global_obj
from serve.publish_product import publish_product_main
from tokens.get_token import get_current_user_token
from update_data_to_tk.util.create_request_body import get_json
from util.mysql_util.insert_data import sql_executor_dml
from util.tk_connection_util.get_sign_from_url import generate_signature


def create_data_json_to_tk(title, description, img_arr, weight, high, width, length, sku, product_id, href, sku_data):
    """
    创建格式正确的json字符串，透传到tk上
    :param sku_data:
    :param attr:
    :param href:
    :param product_id:
    :param sku:
    :param length:
    :param width:
    :param high:
    :param weight:
    :param img_arr:
    :param description:
    :param title:英文标题
    :return:
    """
    # 获取当前用户的唯一标识,唯一标识，表示是给哪个店铺上品的，和mysql的tk_user_token_msg自增id对齐
    token = get_current_user_token()
    # 符合预期的情况下
    request_body = get_json(title, description, img_arr, weight, high, width, length, sku)
    app_key = global_obj.production_conf['tk_util']['app_key']
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }

    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_products?timestamp={timestamp}&app_key={app_key}"
    request = requests.Request(method="POST", url=url, headers=headers, json=request_body)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    logging.info(f"sign计算成功，进行数据请求rul: {url_finally}")
    response = requests.post(url_finally, headers=headers, json=request_body)
    print(response.text)
    if response.status_code == 200 and response.json()['message'].lower() == 'success':
        # sql写入数据到数据库当中
        logging.info("请求成功")
        user_id = int(global_obj.production_conf['shop_id'])
        upload_product_data_to_db(href, product_id, user_id, title, weight, high, width, length, description)
        # 更新sku的信息skuid以及对应的价格信息等
        # update_sku_to_db(response.json())
        if global_obj.production_conf['public_product'] == 'true' or global_obj.production_conf['public_product'] is True:
            publish_product_main(response.json())
        logging.info("上品完成，且写入到数据库当中了")

    else:
        logging.info("上品失败啦～")


def upload_product_data_to_db(href, product_id, user_id, title, weight, high, width, length, detail_html):
    """

    :param href:
    :param product_id:
    :param user_id:
    :param title:
    :param weight:
    :param high:
    :param width:
    :param length:
    :param detail_html:
    :return:
    """
    ts = int(time.time())
    load_sql = f"""
    insert into product_detail_1688 (url, original_id, user_id, title, weight, high, width, length, detail_html,
     create_time, modify_time)
     values('{href}', '{product_id}', {user_id}, '{title}', {weight}, {high}, {width}, {length}, '{detail_html}', {ts}, {ts});
    """
    response = sql_executor_dml(load_sql)
    if response == 'success':
        logging.info("数据写入成功")
    else:
        logging.warning("最终数据写入失败")


def update_sku_to_db(response_data):
    """
    返回数据结果sku信息写入到数据库当中，使用的主键是seller_sku
    :param response_data:  返回结果
    :return:
    """
    skus = response_data['data']['global_skus']
    for sku in skus:
        global_product_id = sku['id']
        seller_id = sku['seller_sku']
        sql = f"""
        update sku_data_detail
         set global_sku_id = '{global_product_id}'
         where id = {seller_id};
        """
        response = sql_executor_dml(sql)
        if response == 'success':
            logging.info("sku数据更新成功")
        else:
            logging.info("sku信息更新失败")


