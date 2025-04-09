# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_token.py
@Author   :wangmaosheng
@Date     : 2025/2/4 21:53
@Desc:    : 获取token，请求的时候使用到
"""
import logging

from global_data import global_obj
from util.mysql_util.select_data import sql_search_all


def get_current_user_token():
    """
    通过配置文件获取当前用户的token
    :return:tokens: 用户令牌数据
    """
    shop_id = global_obj.production_conf['shop_id']
    select_shop_token_sql = f"""
    select access_token from tk_user_token_msg
    where id = {shop_id}
    """
    logging.info(f"获取当前token信息: shop_id: {shop_id}")
    result_data = sql_search_all(select_shop_token_sql)
    if len(result_data) == 1:
        token = result_data[0][0]
        logging.info(f"token为： {token}")
        return token
    else:
        logging.error(f"token获取错误，获取数据库数据为：{result_data}")
        raise ValueError("token获取失败了")
