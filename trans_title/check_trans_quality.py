# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : check_trans_quality.py
@Author   :wangmaosheng
@Date     : 2025/3/22 22:42
@Desc:    : 校验翻译数据质量
"""
import sys

import pandas
import pandas as pd
from openai import OpenAI


def check_quality(data):
    array_list = data.values.tolist()
    client = OpenAI(api_key="sk-GTGubExJacM9sZtP084e29681b28471e883921702e341fE2",
                    base_url="https://api.linkapi.org/v1")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "你读取的是一个二维数组，其中第二列和第三列是基于第四列的英文翻译成的小语种，希望你帮我分析一下，第二列和第三列到底那一列翻译的效果更好呐，比如满分100分的话，分别站在电商卖家的角度给两个店铺客观的进行打分"},
            {"role": "user", "content": f"{array_list}"},
        ],
        stream=False,
        temperature=1.0
    )
    res_data = response.choices[0].message.content

    print(response)

    print("*******")
    print(res_data)
    return res_data
#
# data = pd.read_excel("./result.xlsx", sheet_name="Sheet1")
# array_list = data.values.tolist()
# # print(array_list)
#
# # sys.exit(1)
#
# client = OpenAI(api_key="sk-GTGubExJacM9sZtP084e29681b28471e883921702e341fE2",
#                 base_url="https://api.linkapi.org/v1")
#
# # print("开始分析")
# response = client.chat.completions.create(
#     model="deepseek-r1",
#     messages=[
#         {"role": "system", "content": "你读取的是一个二维数组，其中第二列和第三列是基于第四列的英文翻译成的小语种，希望你帮我分析一下，第二列和第三列到底那一列翻译的效果更好呐，比如满分100分的话，分别站在电商卖家的角度给两个店铺客观的进行打分"},
#         {"role": "user", "content": f"{array_list}"},
#     ],
#     stream=False,
#     temperature=1.0
# )
# print("分析完成")
# res_data = response.choices[0].message.content
#
# print(response)
#
#
# print("*******")
# print(res_data)
#
#
