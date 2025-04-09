# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : add_head_and_tail.py
@Author   :wangmaosheng
@Date     : 2025/3/29 23:04
@Desc:    : 在商品描述当中添加开头和结束的img图，提升店铺形象
"""


import pandas as pd
from bs4 import BeautifulSoup
import sys
import html


input_path = "/Users/wangmaosheng/Desktop/sg_data.xlsx"
begin_img = 'https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/65e5b083c2c248179ef25b23e40135d3~tplv-o3syd03w52-origin-jpeg.jpeg?dr=15568&from=1432613627&idc=maliva&ps=933b5bde&shcp=9cd7d13a&shp=5563f2fb&t=555f072dwidth=1598&height=1284'
finally_flag = "https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/d76a11d52df54447a41f2516889b7b45~tplv-o3syd03w52-origin-jpeg.jpeg?dr=15568&from=1432613627&idc=maliva&ps=933b5bde&shcp=9cd7d13a&shp=5563f2fb&t=555f072dwidth=1592&height=1154"
input_data = pd.read_excel(input_path, sheet_name="Template")

for index, every_line_desc in input_data.iterrows():
    desc = str(every_line_desc['product_description'])
    soup = BeautifulSoup(desc, 'html.parser')
    print(f"修改前 {desc}")

    img_tags = soup.find_all('img')
    # 确保有img标签
    if img_tags:
        # 获取第一个和最后一个img标签
        first_img = img_tags[0]
        last_img = img_tags[-1]
        # 创建新的img标签
        if first_img.get("src") == begin_img or last_img.get("src") == last_img:
            print("已经替换过了，跳过")
            continue
        new_img_before_first = soup.new_tag('img', src=begin_img, width='800', height='600')
        new_img_after_last = soup.new_tag('img', src=finally_flag, width='800', height='600')
        # 在第一个img标签前插入新的img标签
        first_img.insert_before(new_img_before_first)

        # 在最后一个img标签后插入新的img标签
        last_img.insert_after(new_img_after_last)

        # 输出修改后的HTML
        finally_soup_str = html.unescape(soup)
        print(f"修改后的标签：{html.unescape(soup)}")
        every_line_desc['product_description'] = finally_soup_str
    else:
        print('页面中没有找到任何img标签。')

input_data.to_excel("/Users/wangmaosheng/Desktop/sg_change_desc.xlsx", sheet_name="Template", index=False)




