# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : load_1688_data_parse.py
@Author   :wangmaosheng
@Date     : 2025/1/25 17:27
@Desc:    :将1688数据源的数据进行解析处理
"""
import json
import sys

from openai import OpenAI
import logging
import time
import re
import requests
import threading
from PIL import Image
from io import BytesIO

from tornado import concurrent

from global_data import global_obj
from serve.parse_util.get_description import get_description
from serve.parse_util.get_product_attributes import get_global_attribute
from serve.parse_util.get_property import get_product_message
from serve.parse_util.get_skus import sku_data_to_object
from serve.parse_util.main_imgs import get_img_url_from_1688_data
from update_data_to_tk.upload_product_to_tk import create_data_json_to_tk
from util.mysql_util.select_data import sql_search_all

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_lock = threading.Lock()


def data_1688_parse():
    """
    获取到的1688的原始数据，和前端js远程脚本相呼应, 通过读取线程间队列进行数据的处理，防止任务阻塞
    :return: 进行格式转换过滤后-先进行输出
    """
    while True:
        # 队列为空的话就一直等待
        while global_obj.task_queue.empty():
            time.sleep(global_obj.global_config['service']['wait_ts'])
        data = global_obj.task_queue.get()
        # 需要判断当前url是否已经处理过了
        if is_updated(data):
            product_id = re.search(r'(?<=offer/)(\d+)', data['page_url']).group(1)

            # sku 信息
            sku = sku_data_to_object(data['skus_format'], product_id)
            if sku is None:
                continue
            href = data['page_url']
            # 处理主照片
            img_uri = get_img_url_from_1688_data(data)
            # 处理标题
            description = get_description(data)
            if description is None:
                return
            title = data['title']
            english_title = parse_title(title)
            if english_title is None:
                logging.error(f"商品标题解析不出来：{title}")
                return
            logging.info(f"product_id: {product_id}  title: {english_title} href: {href}")
            # 商品属性信息
            # attr = get_global_attribute()
            # 商品的重量和尺寸信息
            weight, high, width, length = get_product_message(data)
            create_data_json_to_tk(english_title, description, img_uri, weight, high, width, length, sku, product_id,
                                   href,
                                    data['skus_format'])
        else:
            logging.info("该商品已上传过了哦")
        global_obj.task_queue.task_done()


def parse_title(title):
    """
    解析文章标题为英文
    :param title: 传入的中文标签
    :return: 英文版的标题
    """
    logging.info(f"原文+{title}")
    client = OpenAI(api_key=global_obj.gpt_conf['title_gpt']['api'],
                    base_url=global_obj.gpt_conf['title_gpt']['base_url'])

    title_format = global_obj.gpt_conf['title_gpt']['title_format']
    response = client.chat.completions.create(
        model=global_obj.gpt_conf['title_gpt']['gpt_module'],
        messages=[
            {"role": "system", "content": "你是一个英文水平很好，且经验丰富的跨境电商店主"},
            {"role": "system", "content": title_format},
            {"role": "user", "content": title},
        ],
        stream=False
    )
    res_data = response.choices[0].message.content
    if response.choices[0].finish_reason == 'stop':
        return res_data
    else:
        return None


def is_updated(data):
    """
    当前商品是否在该商店是否已经上传，避免重复上传的问题
    :param data:  1688采集的数据
    :return:  boolean 类型
    """
    href = data['page_url']
    product_id = re.search(r'(?<=offer/)(\d+)', href).group(1)
    shop_id = global_obj.production_conf['shop_id']
    sql = f"""
    select `id` from product_detail_1688 where user_id = {shop_id} and original_id = {product_id};
    """
    products = sql_search_all(sql)
    if products is None or len(products) == 0:
        return True
    else:
        logging.warning("当前商品已经上传了，不能重复上传了")
        return False


# def third_update_data(data):
#     """
#     多线程任务处理
#     :param data:
#     :return:
#     """
#