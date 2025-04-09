# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : global_obj.py
@Author   :wangmaosheng
@Date     : 2025/1/26 02:21
@Desc:    :
"""
import logging
from concurrent.futures import ThreadPoolExecutor
import queue
from airflow.utils import yaml

# 全局变量
global_config = None
task_queue = None
executor = None
global_DB_conf = None
gpt_conf = None
production_conf = None


def init_global_conf():
    """
    进行全局变量的初始化
    :return:
    """
    global global_config, global_DB_conf, gpt_conf, production_conf
    global_config, global_DB_conf, production_conf, gpt_conf = get_conf_data()
    global task_queue
    task_queue = queue.Queue(maxsize=global_config['service']['queue_size'])
    # 线程池最大线程数
    global executor
    executor = ThreadPoolExecutor(max_workers=global_config['service']['max_workers'])


def get_conf_data():
    """
    读取 YAML 文件
    :return: yml文件
    """
    with open("conf/conf.yml", "r") as file:
        config = yaml.safe_load(file)
    with open("conf/mysql.yml", "r") as file:
        mysql_conf = yaml.safe_load(file)
    target_file = config['use_which_yml']
    logging.info(f"target_file: {target_file}")
    with open(f"conf/{target_file}/conf.yml", "r") as file:
        product_conf = yaml.safe_load(file)
    with open(f"conf/{target_file}/gpt.yml", "r") as file:
        gpt_conf = yaml.safe_load(file)
    return config, mysql_conf, product_conf, gpt_conf
