# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_description.py
@Author   :wangmaosheng
@Date     : 2025/2/4 21:51
@Desc:    : desc描述信息的获取和补全，可能会用到gpt进行处理
"""
import logging
import random
import time
from io import BytesIO
from PIL import Image
import threading
import requests
from openai import OpenAI

from global_data import global_obj
from util.tk_connection_util.get_sign_from_url import generate_signature
from tokens.get_token import get_current_user_token


def get_description(data):
    """
     获取描述信息，并且将其中的中文转换为对应英文
    :param data:  传入的描述信息
    :return:
    """
    imgs = data['detail_img']['imgs']
    logging.info(f"imgs: {imgs}")
    detail_arr = []
    for img in imgs:
        try:
            if img.find("?__r__") != -1:
                src = img.split("?__r__")[0]
            else:
                src = img
            if global_obj.production_conf['check_desc_img'] == 'true' or global_obj.production_conf['check_desc_img'] is True:
                detail_url = is_judge_img(src)
                if detail_url is not None:
                    detail_arr.append(detail_url)
            else:
                detail_url = upload_detail_img(src, "DESCRIPTION_IMAGE")
                detail_arr.append(detail_url)
        except (Exception, IOError, TimeoutError):
            logging.error(f"照片: {img} 下载错误异常")
    logging.info(f"描述信息当中的图片筛选并处理完成,进行detail描述信息html的生成 detail_arr: {detail_arr}")
    html_detail = html_description(detail_arr)
    logging.info(f"商品信息html： {html_detail}")
    return html_detail


def is_judge_img(url):
    """
    通过gpt帮我判断当前的图是否适用于电商网站
    :param url: 网络图片的url，1688平台图片
    :return:
    """
    client = OpenAI(api_key=global_obj.production_conf['img_judge_gpt']['api'],
                    base_url=global_obj.production_conf['img_judge_gpt']['base_url'])

    system_role = global_obj.gpt_conf['img_judge_gpt']['system_role']
    response = client.chat.completions.create(
        model=global_obj.gpt_conf['img_judge_gpt']['gpt_module'],
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content":
                [
                    {"type": "image_url",
                     "image_url": {
                         "url": f"{url}"
                     }
                     }
                ]
             },
        ],
        stream=False,
        temperature=1.0
    )
    res_data = response.choices[0].message.content
    logging.info(f"图片 {url} 处理完成，处理结果为:  {res_data}")
    if response.choices[0].finish_reason == 'stop':
        # 将符合要求的照片上传上去之后获取url和uri等信息
        if res_data.find('true') != -1 or res_data.find('true_1') != -1 or res_data.find('true_2') != -1:
            return upload_detail_img(url, "DESCRIPTION_IMAGE")
        else:
            return None
    else:
        return None


def upload_detail_img(src, use_case="DESCRIPTION_IMAGE"):
    """
    将描述当中的src内容写入到tiktok当中，获取uri
    :param use_case: 用户类别
    :param src: url
    :return:
    """
    jpeg_img = update_img_use_tk_api(src)
    if jpeg_img is None:
        return None
    token = get_current_user_token()
    headers = {
        "x-tts-access-token": token
    }
    re_data = {
        "use_case": use_case
    }
    files = {'data': (f'image.jpg_{random.randint(100, 20000)}', jpeg_img, 'image/jpeg')}  # 这里用 image.jpg 是因为上传需要一个文件名
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    app_key = global_obj.production_conf['tk_util']['app_key']
    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/images/upload?app_key={app_key}&timestamp={timestamp}"
    request = requests.Request(method="POST", url=url, headers=headers, files=files, data=re_data)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    response = requests.post(url_finally, headers=headers, files=files, data=re_data)
    if response.status_code == 200:
        url_msg = response.json()
        ur = {"uri": url_msg['data']['uri'],
              "url": url_msg['data']["url"]
              }
        logging.info(f"uri: {ur}")
        return ur
    else:
        logging.error("当前照片上传失败了哦～ ")
        logging.info(f"失败的response返回: {response.text}")
        return None


def update_img_use_tk_api(img_url):
    """
    从网络当中获取照片，在gpt当中进行判断，然后上传到tk上，获取对应的url和uri，不存储到数据库当中，只在当前的内存当中保存
    :param img_url: 图片的url链接
    :return:  图片下载下来的二进制
    """
    logging.info("进入网络请求图片中")
    # 伪装浏览器头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://detail.1688.com/offer/688371202837.html?spm=a260k.27118904.m2eeca9u.2.6fdbce5c9VJjAj",
        "content-type": "image/jpeg",
    }
    response = requests.get(img_url, headers=headers)
    logging.info(f"获取成功 {response.status_code}")
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer.getvalue()
    else:
        return None


def html_description(img_arr):
    """
    生成html
    :param img_arr: 解析后的url信息了
    :return:
    """
    url_list = [img_ar["url"] for img_ar in img_arr]
    html_detail = "<div> \n"
    for url in url_list:
        img_one = f'<img src = "{url}" />'
        html_detail += img_one
    html_detail += "</div>"
    return html_detail


def timeout():
    """
    执行超时之后执行语句
    :return:
    """
    logging.info("GPT分析图片执行超时")
