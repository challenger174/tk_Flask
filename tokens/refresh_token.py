# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : refresh_token.py
@Author   :wangmaosheng
@Date     : 2025/2/4 20:46
@Desc:    : token刷新任务
"""
import logging
import time
import requests

from global_data import global_obj
from util.mysql_util.insert_data import sql_executor_dml
from util.mysql_util.select_data import sql_search_all


def token_refresh():
    """
    刷新token线程，定期进行token检测，进行token刷新
    :return: 无返回值
    """
#     获取满足要求时间戳的所有用户信息，大概离过期还剩两天的时候进行刷新
    while True:
        logging.info("续签循环中")
        sleep_time = global_obj.production_conf['tk_util']['refresh_frequency']
        if sleep_time is None:
            logging.error("时间参数有问题, token刷新失败")
            return None
        current_time = int(time.time())
        # 过期时间小于3天就要进行续约
        sql = f"""
            select id,access_token,access_token_expire_in,refresh_token,refresh_token_expire_in,open_id,seller_name,
                    seller_base_region,user_type from tk_user_token_msg 
                where LEAST(access_token_expire_in,refresh_token_expire_in) - {current_time}  <=  172800
                AND LEAST(access_token_expire_in,refresh_token_expire_in) - {current_time} > 0
        """
        response_data = sql_search_all(sql)
        if response_data is not None:
            for response in response_data:
                app_secret = global_obj.production_conf['tk_util']['app_secret']
                app_key_conf = global_obj.production_conf['tk_util']['app_key']
                request_url = f"https://auth.tiktok-shops.com/api/v2/token/refresh?app_key={app_key_conf}" \
                              f"&app_secret={app_secret}" \
                              f"&refresh_token={response[3]}" \
                              "&grant_type=refresh_token"
                id_uniq = response[0]
                net_work_respon = requests.get(request_url)
                print(f"data:1 {net_work_respon.json()}")
                if net_work_respon.status_code == 200 and net_work_respon.json()['message'] == 'success':
                    logging.info("续签请求发送成功，更新数据库中")
                    data = net_work_respon.json()
                    access_token = data['data']['access_token']
                    access_token_expire_in = data['data']['access_token_expire_in']
                    refresh_token = data['data']['refresh_token']
                    refresh_token_expire_in = data['data']['refresh_token_expire_in']
                    open_id = data['data']['open_id']
                    seller_name = data['data']['seller_name']  # 卖家店铺名称
                    seller_base_region = data['data']['seller_base_region']  # 店铺所在的国家
                    user_type = data['data']['user_type']  # 用户类型：0:卖家 1:创作者 3:合作伙伴
                    current_time = int(time.time())
                    update_sql = f"""
                        update tk_user_token_msg set
                            access_token = '{access_token}',
                            access_token_expire_in = {access_token_expire_in},
                            refresh_token = '{refresh_token}',
                            refresh_token_expire_in = {refresh_token_expire_in},
                            open_id = '{open_id}',
                            seller_name = '{seller_name}',
                            seller_base_region = '{seller_base_region}',
                            user_type = {user_type},
                            modify_time = {current_time}
                        where id = {id_uniq}
                    """
                    response = sql_executor_dml(update_sql)
                    if response == 'success':
                        logging.info("续签成功")
                    else:
                        logging.error("续签失败")
                else:
                    logging.error("续签失败")
        else:
            logging.info("没有即将过期的token")
        logging.info("进入等待时间循环时间")
        time.sleep(int(sleep_time))  # 休眠时间
