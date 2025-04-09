# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : change_local_langage.py
@Author   :wangmaosheng
@Date     : 2025/3/23 10:46
@Desc:    :小语种的切换
"""
import io
import random

import pandas
import pandas as pd

# 先随机切换两百个
# random_cnt = 200
# size = 0
# mapping = {}
# input_file = "/Users/wangmaosheng/Desktop/result 2.xlsx"
# output_file = "/Users/wangmaosheng/Desktop/th_change_200.xlsx"
# th_data = "/Users/wangmaosheng/Desktop/th_data.xlsx"


def pipei_data(mapping_orical, local_data):
    mapping = {}
    for index, row in mapping_orical.iterrows():
        mapping[str(row['product_id'])] = row['trans_title']

    for index, row in local_data.iterrows():
        product_id = row['product_id']
        if mapping.get(product_id) is not None:
            row['product_name'] = mapping.get(product_id)
            row['product_property/100177'] = 'No'

    local_data.to_excel("nv_title_youhua", index=False,sheet_name='Template')
    # excel_file = io.BytesIO()
    # local_data.to_excel(excel_file, index=False, engine='openpyxl')  # 写入字节流
    # excel_file.seek(0)
    # return excel_file

# mapping_orical = pd.read_excel(input_file, sheet_name="Sheet1")

# for index, row in mapping_orical.iterrows():
#     rand = random.randint(0, 50)
#     if rand <= 20 and size < 200:
#         size = size + 1
#         mapping[str(row['product_id'])] = row['trans_title']
#     else:
#         pass

# th = pd.read_excel(th_data, sheet_name="Template")
# for index, row in th.iterrows():
#     product_id = row['product_id']
#     if mapping.get(product_id) is not None:
#         row['product_name'] = mapping.get(product_id)
#         row['product_property/100177'] = 'No'
#
# th.to_excel(output_file, sheet_name='Template', index=False)
#


