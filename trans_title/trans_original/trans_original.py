# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : trans_original.py
@Author   :wangmaosheng
@Date     : 2025/3/29 00:15
@Desc:    :
"""
import threading
import pandas as pd
from bs4 import BeautifulSoup
from googletrans import Translator
from openai import OpenAI


language = "泰语"
input_file = "/Users/wangmaosheng/Desktop/golbal_base.xlsx"
# 单独国家的倒出的excel
input_file_area = "/Users/wangmaosheng/Desktop/th_data.xlsx"
output_file = f"/Users/wangmaosheng/Desktop/output_{language}.xlsx"
# system_role = f"你是一名懂得各种小语种的电商专家，现在需要将英文标题翻译成对应的{language}标题，希望在转换的时候能够适当润色标题，提升商品的SEO,最后将标题当" \
#               f"中的逗号用空格代替，只返回对应语言的结果，不需要额外的输出"
system_role = f"""你是一名专注于东南亚电商的SEO翻译专家，任务是将英文商品标题翻译成{language}，要求：
            1. 精准保留核心关键词并本地化；
            2. 符合目标语言搜索习惯；
            3. 避免文化冲突词汇；
            5. 字符数控制在平台要求内250个字符内。
            6. 最终只输出标题结果，不需要其他解释字符
            7. 需要将翻译之后的逗号用空格替换掉，保持工整
            8. 需考虑tiktok算法SEO偏好 权重等问题，尽可能提升索搜和曝光"""
sheet_name = "Template"
third_size = 70

trans_arr = []
lock = threading.Lock()


def get_src_arr(hmtl_descip):
    """
    返回 商品描述页面的src的数组
    :param hmtl_descip:
    :return:
    """
    soup = BeautifulSoup(hmtl_descip, 'html.parser')
    img_arr = [img['src'] for img in soup.find_all('img')]
    img_list = img_arr[1:-1]
    return ",".join(img_list)


def gtp_translate(part_data, index):
    """
    传入英文标题，翻译成指定语言
    :return:
    """
    client = OpenAI(api_key="sk-GTGubExJacM9sZtP084e29681b28471e883921702e341fE2",
                    base_url="https://api.linkapi.org/v1")
    for i in part_data[index]:
        product_id = i[0]
        local_language = i[1]
        global_language = i[2]
        global_product_id = i[3]
        if global_language is not None or global_language != "" or len(global_language) >= 10:
            response = client.chat.completions.create(
                model="deepseek-v3",
                messages=[
                    {"role": "system", "content": f"{system_role}"},
                    {"role": "user", "content": f"{global_language}"},
                ],
                stream=False,
                temperature=1.0
            )
            res_data = response.choices[0].message.content
            print(f"product_id: {product_id} gpt-4o : {res_data}")
            with lock:
                trans_arr.append((product_id, local_language, res_data, global_language, global_product_id))
        else:
            print("不进行修改")
            with lock:
                trans_arr.append((product_id, local_language, local_language ,global_language, global_product_id))

    return trans_arr


df = pd.read_excel(input_file, sheet_name=sheet_name)
description = df['product_description'][5:]
# 全球商品的描述src信息
all_products_mig_src = description.apply(get_src_arr)
df['img_list'] = all_products_mig_src
# print(df.columns)
# print(df.shape)
df = df.drop_duplicates(subset=['img_list'])
print("主表进行去重")
print(df.shape)
# 如果差值是5的话是复合预期的，因为excel的前5行是平台指定的行，所以可以理解为没有重复

area_product_excel = pd.read_excel(input_file_area, sheet_name=sheet_name)
area_desc = area_product_excel['product_description'][4:]
area_product_excel['img_list'] = area_desc.apply(get_src_arr)
# print(area_product_excel.columns)
# print(area_product_excel.shape)
product_id_list = area_product_excel.drop_duplicates(subset=['product_id'])

new_data = []
df_merge = product_id_list.merge(df, on="img_list", how="left")
# print(df_merge.columns)
# test = df_merge[['product_id', 'img_list', 'product_name_x', 'global_product_id', 'product_name_y']]
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# # test_1 = test[test['product_name_y'].isna()]
# # test_1.drop_duplicates(subset=['product_id'])
# # test_1.to_csv("out.txt", sep=",", index=True)
out_arr = [[] for _ in range(third_size)]
for index, row in df_merge[df_merge['product_name_y'].notna()].iterrows():
    if row['product_id'].isdigit():
        out_arr[index % third_size].append((row['product_id'], row['product_name_x'], row['product_name_y'], row['global_product_id']))

threads = []
for i in range(third_size):
    t = threading.Thread(target=gtp_translate, args=(out_arr, i))
    # t = threading.Thread(target=facebook_trans, args=(out_arr, i))
    threads.append(t)
    t.start()

for i in threads:
    i.join()


df = pd.DataFrame(trans_arr, columns=["product_id", 'local_title', 'trans_title', 'english_title', "global_product_id"])
df.to_excel("result.xlsx", index=False)
