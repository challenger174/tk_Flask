# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_skus.py
@Author   :wangmaosheng
@Date     : 2025/2/5 01:03
@Desc:    :sku信息创建，返回一个数组dict
"""
import logging
import re

from openai import OpenAI

from global_data import global_obj
from serve.parse_util.get_description import upload_detail_img
from util.mysql_util.insert_data import sql_executor_dml
from util.mysql_util.select_data import sql_search_all


def sku_data_to_object(skus, product_id):
    """
    sku信息封装为可以透传的json
    :param product_id:
    :param skus:sku信息
    :return:
    """
    sku_data = []
    logging.info(f"sku信息处理中")
    if str(skus['data_stye']) == '1':
        for sku in skus['skus']:
            if sku['sku_img'] is None or sku['sku_img'] == '':
                continue
            logging.info(f"进入sku当中： {sku}")
            sku_img = {"uri": re.sub("_sum.jpg", "", sku['sku_img'])}
            sku_name = sku['sku_name']
            # 销售属性信息
            attr = sales_attributes(sku_name, sku_img)
            global_quantity = int(global_obj.production_conf['product']['global_product_quantity'])
            # 自定义sku信息，从0开始
            seller_sku = get_current_user_define_sku()
            price_calculate = global_obj.production_conf['price_format']
            price_calculate_double = global_obj.production_conf['price_double_format']
            pattern = r"\d{1,3}(?:,\d{3})*(?:\.\d+)?"
            prices = re.findall(pattern, sku['sku_price'])
            prices = [price.replace(",", "") for price in prices]
            if float(prices[0]) <= 3:
                new_calcu_str = re.sub("price", prices[0], price_calculate)
                price_show = str(round(eval(new_calcu_str), 2))
            else:
                new_calcu_str = re.sub("price", prices[0], price_calculate_double)
                logging.info(f"价格计算公式为：{new_calcu_str}")
                # 保留两位小数，单位是美元
                price_show = str(round(eval(new_calcu_str), 2))
            price = {
                "amount": price_show,
                "currency": "USD"
            }
            object_one = {
                "sku_img": sku_img,
                "price": price,
                "global_quantity": global_quantity,
                "sales_attributes": attr,
                "seller_sku": seller_sku+"_"+prices[0]+"_"+product_id
            }
            sku_data.append(object_one)
            insert_sku_data(product_id, float(price_show), attr[0]['sku_img']['uri'], prices[0], seller_sku)
        return sku_data
    elif str(skus['data_stye']) == '2':
        logging.info("复杂sku解析")
        skus_detail = get_mulitple_attributes(skus['skus'], product_id)
        logging.info("sku信息处理完成")
        return skus_detail


def sales_attributes(sku_name, sku_url):
    """
    销售属性：相当于数据页面的不同的sku信息
    :return: dict数组
    """
    sales_attributes_arr = []
    client = OpenAI(api_key=global_obj.gpt_conf['sku_data_trans']['api'],
                    base_url=global_obj.gpt_conf['sku_data_trans']['base_url'])

    system_role = global_obj.gpt_conf['sku_data_trans']['system_role']
    response = client.chat.completions.create(
        model=global_obj.gpt_conf['sku_data_trans']['gpt_module'],
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": f"{sku_name}"}

        ],
        stream=False,
        temperature=1.0
    )
    if response.choices[0].finish_reason == 'stop':
        english_sku_name = response.choices[0].message.content
        obj_data = {
            "name": "Style",
            "value_name": english_sku_name,
            "sku_img": {
                "uri": sku_img_update_load(sku_url['uri'])['uri']
            }
        }
        sales_attributes_arr.append(obj_data)
    return sales_attributes_arr


def sku_img_update_load(sku_url):
    """
    返回rul和 uri
    :param sku_url:
    :return:
    """
    response = upload_detail_img(sku_url, "ATTRIBUTE_IMAGE")
    return response


def get_current_user_define_sku():
    """
    返回递增的sku信息
    :return:
    """
    sql = """
    select max(id) from sku_data_detail;
    """
    response = sql_search_all(sql)
    if response is None or response[0][0] is None or len(response) == 0:
        return "1"
    else:
        return str(response[0][0]+1)


def insert_sku_data(product_id, price, uri, purchas_price, seller_sku):
    """
    数据写入到mysql当中
    :param purchas_price: 采购价格，中文
    :param product_id:
    :param price:
    :param uri:
    :return:
    """
    insert_sql = f"""
    insert into sku_data_detail (id, product_id, price, uri, purchase_price) values({seller_sku}, '{product_id}', {price}, '{uri}', {purchas_price});
    """
    response = sql_executor_dml(insert_sql)
    if response == 'success':
        logging.info("sku写入成功")
    else:
        logging.error("sku写入失败")


def transform(sku_name):
    """
    销售属性：返回翻译结果
    :return: dict数组
    """
    sales_attributes_arr = []
    client = OpenAI(api_key=global_obj.gpt_conf['sku_data_trans']['api'],
                    base_url=global_obj.gpt_conf['sku_data_trans']['base_url'])

    system_role = global_obj.gpt_conf['sku_data_trans']['system_role']
    response = client.chat.completions.create(
        model=global_obj.gpt_conf['sku_data_trans']['gpt_module'],
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": f"{sku_name}"}

        ],
        stream=False,
        temperature=0.5
    )
    if response.choices[0].finish_reason == 'stop':
        english_sku_name = response.choices[0].message.content
        return english_sku_name
    else:
        return None


def get_mulitple_attributes(skus, product_id,):
    """
    生成多属性的sku的对应的数据访问
    :param skus: 多属性的双层嵌套skus
    :return:
    """
    skus_obj = []
    index = 0
    transform_tag = []
    global_quantity = int(global_obj.production_conf['product']['global_product_quantity'])
    for outer_sku in skus:
        logging.info("外层循环")
        label_1_img_url = outer_sku['img_url']
        label_1_name = outer_sku['name']
        sku_img = {"uri": re.sub("_sum.jpg", "", label_1_img_url)}
        response_img = sku_img_update_load(sku_img['uri'])['uri']
        label_1_name_english = transform(label_1_name)
        clolr_attr = {
            "name": "Color",
            "value_name": label_1_name_english,
            "sku_img": {
                "uri": response_img
            }
        }
        index += 1
        len = 0
        for inner_sku in outer_sku['child_skus']:
            logging.info("内层循环")
            label_2_name = inner_sku['name']
            label_2_price = inner_sku['sku_price']
            seller_sku = get_current_user_define_sku()
            price_calculate = global_obj.production_conf['price_format']
            price_calculate_double = global_obj.production_conf['price_double_format']
            pattern = r"\d{1,3}(?:,\d{3})*(?:\.\d+)?"
            prices = re.findall(pattern, label_2_price)
            prices = [price.replace(",", "") for price in prices]
            if float(prices[0]) <= 4:
                new_calcu_str = re.sub("price", prices[0], price_calculate)
                price_show = str(round(eval(new_calcu_str), 2))
            else:
                new_calcu_str = re.sub("price", prices[0], price_calculate_double)
                logging.info(f"价格计算公式为：{new_calcu_str}")
                # 保留两位小数，单位是美元
                price_show = str(round(eval(new_calcu_str), 2))
            if index == 1:
                label_2_name_english = transform(label_2_name)
                transform_tag.append(label_2_name_english)
            else:
                label_2_name_english = transform_tag[len]
            len += 1
            attr_arr = []
            size_attr = {
                "name": "Size",
                "value_name": label_2_name_english
            }
            attr_arr.append(clolr_attr)
            attr_arr.append(size_attr)
            sales_attributes = {
                "global_quantity": global_quantity,
                "sales_attributes": attr_arr,
                "seller_sku": seller_sku + "_" + prices[0]+ "_"+product_id,
                "price": {
                    "amount": price_show,
                    "currency": "USD"
                }
            }
            logging.info("处理单条完成")
            skus_obj.append(sales_attributes)
            insert_sku_data(product_id, float(price_show), clolr_attr['sku_img']['uri'], prices[0], seller_sku)
    logging.info(f"双层嵌套sku信息： {skus_obj}")
    return skus_obj

