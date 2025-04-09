# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_property.py
@Author   :wangmaosheng
@Date     : 2025/2/5 00:37
@Desc:    : 获取属性信息，比如：重量、尺寸等信息
"""
import logging
import re

from global_data import global_obj


def get_product_message(data):
    """
    获取商品的重量等信息相关信息
    :param data: 原始数据
    :return:
    """
    # 重量信息
    logging.info("重量信息处理中")
    if "size" in data:
        # 将重量换算为g
        try:
            is_user_formula = global_obj.production_conf['product']['use_formula']
            if is_user_formula == 'true' or is_user_formula is True:
                weight = int(data["size"]['重量(g)'])
                logging.info(weight)
                formula = global_obj.production_conf['product']['weight_formula']
                weights = re.search(r"\d+", str(weight))
                logging.info(weights.group())
                new_calcu_str = re.sub("weight", weights.group(), formula)
                logging.info(new_calcu_str)
                new_weight = str(round(eval(new_calcu_str), 3))
            else:
                new_weight = str(global_obj.production_conf['product']['default_weight'])
        except KeyError as e:
            new_weight = str(global_obj.production_conf['product']['default_weight'])
    else:
        new_weight = str(global_obj.production_conf['product']['default_weight'])

    high = str(global_obj.production_conf['product']['default_high'])
    width = str(global_obj.production_conf['product']['default_width'])
    length = str(global_obj.production_conf['product']['default_length'])
    logging.info("重量信息处理完成")
    return new_weight, high, width, length
