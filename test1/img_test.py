# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : img_test.py
@Author   :wangmaosheng
@Date     : 2025/2/4 22:14
@Desc:    :
"""
import logging
import random
import sys
import time
from io import BytesIO

import pytesseract
import requests
from PIL import Image
from openai import OpenAI

from serve.parse_util.get_description import update_img_use_tk_api
from tokens.get_token import get_current_user_token
from update_data_to_tk.util.create_request_body import get_category_id
from util.tk_connection_util.get_sign_from_url import generate_signature

if __name__ == '__main__':
    # client = OpenAI(api_key="sk-GTGubExJacM9sZtP084e29681b28471e883921702e341fE2",
    #                 base_url="https://api.linkapi.org/v1")
    #
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Connection": "keep-alive",
    #     "Referer": "https://detail.1688.com/offer/688371202837.html?spm=a260k.27118904.m2eeca9u.2.6fdbce5c9VJjAj",
    #     "content-type": "image/jpeg",
    # }
    # img_url = "https://cbu01.alicdn.com/img/ibank/O1CN01URf8S32NLmbU4dBGc_!!2206371669947-0-cib.jpg"
    # # response = requests.get(img_url, headers=headers)
    # # img = Image.open(BytesIO(response.content))
    # # buffer = BytesIO()
    # # img.save(buffer, format="JPEG")
    # # buffer.seek(0)
    # # data = str(buffer.getvalue())
    # # print("数据获取成功")
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #             {"role": "system", "content": "我向你传入了一个图片url，需要你帮我判断一下，这个图是否适用于tiktok电商当中，判断标准，主要避免中文的出现，如果包含少量【少于6个】中文，返回true_1, 如果不包含中文的商品图，则返回true,如果是一些厂家信息则返回false，如果无法识别，返回true_2, 严格遵守"},
    #             {"role": "user", "content": [
    #                 {"type": "image_url",
    #                  "image_url": {
    #                      "url": "https://cbu01.alicdn.com/img/ibank/O1CN019pQ8Y42NLmfONB9x1_!!2206371669947-0-cib.jpg"
    #                  }
    #                  }
    #             ]},
    #         ],
    #     stream=False,
    #     temperature=1.0
    # )
    # res_data = response.choices[0].message.content
    # print(res_data)
    # img_url = 'https://cbu01.alicdn.com/img/ibank/O1CN01535HNZ2NLmRKXUkPe_!!2206371669947-0-cib.jpg'
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Connection": "keep-alive",
    #     "Referer": "https://detail.1688.com/offer/688371202837.html?spm=a260k.27118904.m2eeca9u.2.6fdbce5c9VJjAj",
    #     "content-type": "image/jpeg",
    # }
    # response = requests.get(img_url, headers=headers)
    # if response.status_code == 200:
    #     print(response.content)
    #     img = Image.open(BytesIO(response.content))
    #     print(1)
    #     buffer = BytesIO()
    #     print(2)
    #     img.save(buffer, format="JPEG")
    #     print(3)
    #     buffer.seek(0)
    #     print(buffer.getvalue())
    # src = 'https://cbu01.alicdn.com/img/ibank/O1CN01535HNZ2NLmRKXUkPe_!!2206371669947-0-cib.jpg'
    # jpeg_img = update_img_use_tk_api(src)
    # if jpeg_img is None:
    #     sys.exit()
    token = "ROW_KfGSqQAAAAAw2cluZXjvtpO9770IY3XUTGN1Nyz2PIJNycag3HUDHiB2uX5B8-SjnZxptkfZ1vlWhG6WaaOzwJGcERXtHBix1WQx03iSaJVrB6CdSvDgXELIM5mgr-C4ROPSUAu2BFz1_RwmWS1d2KelcNZ99sI0nDstJ_bPI1fNcjPrxoLKD6wl-G2Mymk3tfiqo9YqClM"
    # headers = {
    #     "x-tts-access-tokens": token
    # }
    # re_data = {
    #     "use_case": 'DESCRIPTION_IMAGE'
    # }
    # files = {'data': (f'image.jpg_{random.randint(100, 20000)}', jpeg_img, 'image/jpeg')}  # 这里用 image.jpg 是因为上传需要一个文件名
    app_secret = '076ac0a42c25608ed4d7187aece92a20cd813c50'
    app_key = '6em9ajh0nr6ob'
    # timestamp = int(time.time())
    # url = f"https://open-api.tiktokglobalshop.com/product/202309/images/upload?app_key={app_key}&timestamp={timestamp}"
    # request = requests.Request(method="POST", url=url, headers=headers, files=files, data=re_data)
    # sign = generate_signature(request, app_secret)
    # url_finally = url + f'&sign={sign}'
    # logging.info(f"sign计算成功，进行数据请求rul: {url_finally}")
    # response = requests.post(url_finally, headers=headers, files=files, data=re_data)
    # if response.status_code == 200:
    #     url_msg = response.json()
    #     logging.info("上传照片成功")
    #     print(url_msg)
    # else:
    #     logging.error("当前照片上传失败了哦～ ")
    #     logging.info(f"失败的response返回: {response.text}")
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }

    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/global_categories/recommend?app_key={app_key}&timestamp={timestamp}"
    headers = {
        'x-tts-access-token': token,
        'content-type': 'application/json'
    }
    data = {
        "category_version": "v1",
        "product_title": "100 Pcs/Set Hayao Miyazaki Poster Sticker Spirited Away Totoro Creative Decoration Phone Desktop DIY Stickers Ghibli Studio"
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