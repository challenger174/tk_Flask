# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : main_imgs.py
@Author   :wangmaosheng
@Date     : 2025/2/5 00:26
@Desc:    :处理主图
"""
import logging
import re
import requests
from global_data import global_obj
from serve.parse_util.get_description import update_img_use_tk_api
from tokens.get_token import get_current_user_token
from util.tk_connection_util.get_sign_from_url import generate_signature


def get_img_url_from_1688_data(data):
    """
    从透传的1688的数据当中获取得到对应的图片信息
    :param data:  1688当中的数据
    :return: 写入数据库当中
    """
    # 主图
    img_arr = []
    final_arr_uri = []
    img_urls = data['img_urls']
    # 不要video视频，只需要图片就行
    is_video = False
    index = 0
    for i in range(len(img_urls) - 1):
        index = index + 1
        if not is_video:
            if img_urls[i].find("video") != -1 or index > 9:
                continue
            img = re.sub(r'_b.jpg', '', img_urls[i])
            img_arr.append(img)
        else:
            break
    try:
        for img in img_arr:
            if ".png" not in img:
                print(f"img: {img}")
                jpeg_img = update_img_use_tk_api(img)
                uri = send_data_to_tk(jpeg_img)
                if uri is not None:
                    final_arr_uri.append(uri)
    except (Exception, IOError):
        logging.error(f"主图:  下载失败")
    return final_arr_uri


def send_data_to_tk(jpeg_img):
    """
     将数据发送到tk，获取对应的url
    :param jpeg_img: 照片二进制
    :return:
    """
    if jpeg_img is None:
        return None
    token = get_current_user_token()
    headers = {
        "x-tts-access-token": token
    }
    re_data = {
        "use_case": "MAIN_IMAGE"
    }
    files = {'data': ('image.jpg', jpeg_img, 'image/jpeg')}  # 这里用 image.jpg 是因为上传需要一个文件名
    app_secret = global_obj.production_conf['tk_util']['app_secret']
    app_key = global_obj.production_conf['tk_util']['app_key']
    import time
    timestamp = int(time.time())
    url = f"https://open-api.tiktokglobalshop.com/product/202309/images/upload?app_key={app_key}&timestamp={timestamp}"
    request = requests.Request(method="POST", url=url, headers=headers, files=files, data=re_data)
    sign = generate_signature(request, app_secret)
    url_finally = url + f'&sign={sign}'
    logging.info(f"sign计算成功，进行数据请求rul: {url_finally}")
    response = requests.post(url_finally, headers=headers, files=files, data=re_data)
    response_json = response.json()
    if response.status_code == 200:
        uri = {"uri": response_json['data']['uri'],
               "url": response_json['data']['url']
               }
        logging.info(f"上传照片成功 {uri}")
        return uri
    else:
        logging.error("当前照片上传失败了哦～")
        return None
