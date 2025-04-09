# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : change_data_finall.py
@Author   :wangmaosheng
@Date     : 2025/3/29 00:18
@Desc:    :
"""
from random import random

import pandas as pd

# random_cnt = 200
# size = 0
mapping = {}
input_file = "/Users/wangmaosheng/Desktop/result.xlsx"
output_file = "/Users/wangmaosheng/Desktop/th_title_youhua.xlsx"
local_title = "/Users/wangmaosheng/Desktop/th_data.xlsx"

mapping_orical = pd.read_excel(input_file, sheet_name="Sheet1")

for index, row in mapping_orical.iterrows():
    # rand = random.randint(0, 50)
    # if rand <= 20 and size < 200:
    #     size = size + 1
    mapping[str(row['product_id'])] = row['trans_title']
    # else:
    #     pass

th = pd.read_excel(local_title, sheet_name="Template")
for index, row in th.iterrows():
    product_id = row['product_id']
    if mapping.get(product_id) is not None:
        row['product_name'] = mapping.get(product_id)
        row['product_property/100177'] = 'No'

th.to_excel(output_file, sheet_name='Template', index=False)