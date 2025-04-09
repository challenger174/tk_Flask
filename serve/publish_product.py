# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : publish_product.py
@Author   :wangmaosheng
@Date     : 2025/2/12 23:19
@Desc:    : 商品直接进行发布，不在待发布池当中
"""
import logging
import math
import re
import time

import requests

from global_data import global_obj
from tokens.get_token import get_current_user_token
from util.mysql_util.select_data import sql_search_all
from util.tk_connection_util.get_sign_from_url import generate_signature


def publish_product_main(create_data):
    """
    将商品进行上传的主类
    :param create_data: 创建商品时返回的结果
    :return:
    """
    logging.info("进入到publish")
    publish_target = []
    publis_country_list = global_obj.production_conf['public_country']
    skus = create_data['data']['global_skus']
    global_product_id = create_data['data']['global_product_id']
    for publis in publis_country_list:
        publis_country = publis['country']
        price_format = publis['price_format']
        unit = publis['currency']
        logging.info(f"国家发布 {publis_country} {price_format} {unit}")
        skus_arr = []
        for sku in skus:
            logging.info("进入sku配置")
            related_global_sku_id = sku['id']
            seller_sku = sku['seller_sku']
            purchase_price = get_purchase_price(seller_sku)
            if purchase_price is None:
                logging.error("查询原始价格有问题")
                return
            else:
                prices = purchase_price
                new_calcu_str = re.sub("price", str(prices), price_format)
                # 保留一位小数
                price_show = str(math.ceil(eval(new_calcu_str)*10)/10)
                print(f"show price: {price_show}")
                tag = {
                    "related_global_sku_id": related_global_sku_id,
                    "price": {
                        "amount": price_show,
                        "currency": unit
                    }
                }
                skus_arr.append(tag)
        tag_2 = {
            "region": publis_country,
            "skus": skus_arr
        }
        publish_target.append(tag_2)
    public_to_tk_api(publish_target, global_product_id)


def get_purchase_price(seller_sku):
    """
    通过用户自定义的sku表示标识去获取商品的本地价格
    :param seller_sku: 自定义商品sku
    :return:
    """
    get_price_sql = f"""
    select purchase_price from sku_data_detail where id = {seller_sku};
    """
    price_data = sql_search_all(get_price_sql)
    if len(price_data) == 1:
        return price_data[0][0]
    else:
        return None


def public_to_tk_api(publish_target, global_product_id):
    """
    按照tk构建的post数据体
    :param global_product_id: 全球商品id
    :param publish_target:
    :return:
    """
    # 获取当前用户的唯一标识,唯一标识，表示是给哪个店铺上品的，和mysql的tk_user_token_msg自增id对齐
    token = get_current_user_token()
    # 符合预期的情况下
    app_key = global_obj.production_conf['tk_util']['app_key']
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }

    data = {
        "publish_target": publish_target
    }
    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_products/{global_product_id}/publish?app_key={app_key}&timestamp={timestamp}"
    request = requests.Request(method="POST", url=url, headers=headers, json=data)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    logging.info(f"sign计算成功，进行数据请求rul: {url_finally}")
    response = requests.post(url_finally, headers=headers, json=data)
    print(response.text)
    if response.status_code == 200:
        # sql写入数据到数据库当中
        logging.info("请求成功")
        logging.info("上品完成，且写入到数据库当中了")
    else:
        logging.info("上品失败啦～")
