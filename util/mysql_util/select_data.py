# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : select_data.py
@Author   :wangmaosheng
@Date     : 2025/2/4 21:00
@Desc:    : 数据查询
"""
import logging

from global_data import global_obj
import mysql.connector


def sql_search_all(sql):
    """
    查询sql语句，在数据库当中
    :param sql: 查询sql
    :return: 查询到的结果
    """
    db_config = {
        'host': global_obj.global_DB_conf['mysql']['host'],  # 数据库主机地址，'localhost' 或者你的数据库服务器 IP
        'port': global_obj.global_DB_conf['mysql']['port'],
        'user': global_obj.global_DB_conf['mysql']['user'],  # 数据库用户名
        'password': global_obj.global_DB_conf['mysql']['password'],  # 数据库密码
        'database': global_obj.global_DB_conf['mysql']['db']  # 你要连接的数据库名称
    }
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
            logging.info(f"数据查询成功 {all_data}")
            if not all_data or all_data[0][0] is None:
                all_data = None
    except mysql.connector.Error as err:
        logging.error(f"数据写入失败:  {err}")
        all_data = None
    finally:
        # 关闭连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("数据库连接已关闭")
        return all_data
