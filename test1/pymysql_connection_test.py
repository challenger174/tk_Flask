# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : pymysql_connection_test.py
@Author   :wangmaosheng
@Date     : 2025/1/29 17:21
@Desc:    : mysql tk_backstage测试链接
"""
import time

import requests

from global_data import global_obj
import mysql.connector
import logging
import yaml
import json
from urllib.parse import urlparse, parse_qs

from serve.tk_shop_token_message import generate_signature


def sql_search_all_v1(sql):
    db_config = {
        'host': 'rm-bp1hfn11y5r6162vako.mysql.rds.aliyuncs.com' ,  # 数据库主机地址，'localhost' 或者你的数据库服务器 IP
        'port': 3306,
        'user': 'wms_tk',  # 数据库用户名
        'password': 'wms19991216WMS',  # 数据库密码
        'database': 'tk_backstage'  # 你要连接的数据库名称
    }
    print(db_config)
    global all_data, connection, cursor
    all_data = None
    # 连接数据库
    try:
        connection = mysql.connector.connect(**db_config)
        # 检查连接是否成功
        if connection.is_connected():
            # 获取数据库信息
            logging.info(f"数据库链接成功，执行sql语句为：{sql}")
            cursor = connection.cursor()
            cursor.execute(sql)
            all_data = cursor.fetchall()
            logging.info("数据查询成功")
    except mysql.connector.Error as err:
        logging.error(f"数据写入失败:  {err}")
    finally:
        # 关闭连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("数据库连接已关闭")
        return all_data


def get_current_user_token_1():
    """
    通过配置文件获取当前用户的token
    :return:
    """
    shop_id = 1
    select_shop_token_sql = f"""
    select access_token from tk_user_token_msg
    where id = {shop_id}
    """
    result_data = sql_search_all_v1(select_shop_token_sql)
    print(result_data[0][0])
    return result_data[0][0]


def get_global_categories(title):
    """
    通过标题获取当前货品的分类
    :param title:  翻译之后的英文标题
    :return: 对应的分类
    """
    app_key = "6em9ajh0nr6ob"
    app_secret = "076ac0a42c25608ed4d7187aece92a20cd813c50"
    timestamp = int(time.time())
    token = get_current_user_token_1()
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_categories/recommend?app_key={app_key}&timestamp={timestamp}"
    headers = {
        "x-tts-access-token": token,
        "content-type": "application/json"
    }
    data = {
        "product_title": title,
        "category_version": "v1"
    }

    request = requests.Request(method="POST", url=url, headers=headers, json=data)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.post(url_finally, headers=headers, json=data)
    print(response.text)


def get_category_id(categories):
    """
    通过返回的三级类目，进行数据的解析
    :param categories: 数组，需要获取叶子节点的id编号
    :return: 叶子节点编号,和名称
    """
    # global cate_name, cate_id
    # for one in categories:
    #     if one['is_leaf'] and one['level'] == 3:
    #         cate_name = one['name']
    #         cate_id = one['id']

    # return cate_id, cate_name


import base64
import io
import requests
from PIL import Image

def resize_image_from_uri(uri, target_size=(300, 300)):
    if uri.startswith("data:image"):  # 处理 Base64 图片
        header, encoded = uri.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
    elif uri.startswith("http"):  # 处理网络 URL 图片
        response = requests.get(uri)
        image = Image.open(io.BytesIO(response.content))
    else:
        raise ValueError("Unsupported URI format")

    # 调整图片大小
    resized_image = image.resize(target_size, Image.ANTIALIAS)

    # 将处理后的图片转换为 Base64 形式（可嵌入程序）
    buffered = io.BytesIO()
    resized_image.save(buffered, format="PNG")
    base64_str = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{base64_str}"  # 返回 Base64 图片 URI


if __name__ == '__main__':
    resize_image_from_uri("data1")

    # get_global_categories('30Pcs/Box Fairy Tale Little Prince Postcard, Literary Style Holiday Gift Greeting Card Material, Collage Birthday Card Gift')
    # get_global_cate()
    # json_1 = """
    # {"code":0,"data":{"categories":[{"id":"604206","is_leaf":false,"level":1,"name":"Toys \u0026 Hobbies"},{"id":"951560","is_leaf":false,"level":2,"name":"DIY"},{"id":"951688","is_leaf":true,"level":3,"name":"Scrapbooking \u0026 Stamping"}],"leaf_category_id":"951688"},"message":"Success","request_id":"2025012915381351BDCE08CD150E1045B1"}
    # """
    # data = json.loads(json_1)
    # print(data)
    # print(get_category_id(data['data']['categories']))
    # 示例 URI (网络图片 URL 或 Base64)
    # image_uri = "https://cbu01.alicdn.com/img/ibank/O1CN01GFrrS51xovqvpEFvd_!!2216483116491-0-cib.jpg"  # 替换成你的图片链接或 Base64 数据
    # resized_uri = resize_image_from_uri(image_uri)
    # print(resized_uri)  # 这个 URI 可以直接嵌入 HTML 或其他程序中使用
    # urls = ['https://cbu01.alicdn.com/img/ibank/O1CN01IFaXjM2NLmc97bc75_!!2206371669947-0-cib.jpg', 'https://cbu01.alicdn.com/img/ibank/O1CN01lJXnLv2NLmcCRzFr1_!!2206371669947-0-cib.jpg', 'https://cbu01.alicdn.com/img/ibank/O1CN012hJyN52NLmcDrZICd_!!2206371669947-0-cib.jpg', 'https://cbu01.alicdn.com/img/ibank/O1CN01c30QcT2NLmc97bwuM_!!2206371669947-0-cib.jpg', 'https://cbu01.alicdn.com/img/ibank/O1CN01zyJzod2NLmcCRzFqj_!!2206371669947-0-cib.jpg', 'https://cbu01.alicdn.com/img/ibank/O1CN01zjEqX02NLmcC8IwxY_!!2206371669947-0-cib.jpg']
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Connection": "keep-alive",
    #     "Referer": "https://detail.1688.com/offer/688371202837.html?spm=a260k.27118904.m2eeca9u.2.6fdbce5c9VJjAj",
    #     "content-type": "image/jpeg",
    # }
    # for url in urls:
    #     response = requests.get(url, headers=headers)
    #     print(response.status_code)


