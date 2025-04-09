# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : token_register.py
@Author   :wangmaosheng
@Date     : 2025/2/4 20:50
@Desc:    :注册token的信息
"""
import logging
import time

import requests

from global_data import global_obj
from util.mysql_util.insert_data import sql_executor_dml


def create_user_token_and_save(app_key, code):
    """
        用户进行授权之后获取用户相应的auth_code，来计算出token，后续使用的时候也要token,然后将数据存储在mysql当中，因为使用频率不高，
        所以存储在mysql当中没有问题
        :param app_key: 应该是一个唯，其他地方没有使用
        :param code: 获取到的auth_code，有效时间为30min
        :return:
        """
    app_secret = global_obj.global_config['tk_util']['app_secret']
    app_key_conf = global_obj.global_config['tk_util']['app_key']
    print(app_secret)
    print(app_key_conf)
    if app_key_conf == app_key:
        request_token_url = f"https://auth.tiktok-shops.com/api/v2/token/get?app_key={app_key}" \
                            f"&app_secret={app_secret}" \
                            f"&auth_code={code}" \
                            "&grant_type=authorized_code"
        response = requests.get(request_token_url)
        logging.info(response.json())
        if response.status_code == 200 and response.json()['message'] == 'success':
            response_data = response.json()
            if persistence_token(response_data) == 'fail':
                logging.warning("注册时网络请求失败")
                return 'fail'
            else:
                logging.info("网络请求成功")
                return 'success'
        else:
            logging.warning(f"错误码： {response.json()}")
            return "fail"
    else:
        logging.error("获取到的app_key和配置文件当中的不一致，判定为失败")
        return "fail"


def persistence_token(response_data):
    """
    解析出token相关有用的数据之后，将数据存储到mysql数据库当中
    :param response_data:  请求返回结果
    :return:
    """
    access_token = response_data['data']['access_token']
    access_token_expire_in = response_data['data']['access_token_expire_in']
    refresh_token = response_data['data']['refresh_token']
    refresh_token_expire_in = response_data['data']['refresh_token_expire_in']
    open_id = response_data['data']['open_id']
    seller_name = response_data['data']['seller_name']  # 卖家店铺名称
    seller_base_region = response_data['data']['seller_base_region']  # 店铺所在的国家
    user_type = response_data['data']['user_type']  # 用户类型：0:卖家 1:创作者 3:合作伙伴
    current_time = int(time.time())
    sql = f"""
        insert into tk_user_token_msg(seller_name, seller_base_region, user_type, access_token ,access_token_expire_in,
        open_id, refresh_token, refresh_token_expire_in, create_time, modify_time)
        value ('{seller_name}', '{seller_base_region}', {user_type}, '{access_token}', {access_token_expire_in},
        '{open_id}', '{refresh_token}', {refresh_token_expire_in}, {current_time}, {current_time}) 
    """
    logging.info(f"执行插入mysql的sql：{sql}")
    # 将得到的数据写入到mysql数据库当中
    return sql_executor_dml(sql)
