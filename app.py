# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : app.py.py
@Author   :wangmaosheng
@Date     : 2025/1/25 11:06
@Desc:    : 主程序入口
"""
import json
import logging

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

from global_data import global_obj
from serve.load_1688_data_parse import data_1688_parse
from serve.publish_util.get_global_warehouse import get_global_warehouse
from tokens.refresh_token import token_refresh
from tokens.token_register import create_user_token_and_save
from trans_title import trans_title
from util.attributes.get_appributes import get_attribuets
from util.attributes.global_attr import get_global_attributes
import pandas as pd

# 创建 Flask 应用实例
app = Flask(__name__)

# 启用 CORS，允许所有来源的跨域请求
CORS(app)
# 创建多线程间的安全队列，进行数据消费，避免单线程堵塞情况


# 创建一个路由，处理根目录请求
# @app.route('/')
# def hello_world():
#     return get_global_warehouse()


@app.route('/attributes', methods=['GET'])
def get_attributes():
    """
    获取商品属性相关数据，如果不知道当前店铺所属类目有哪些属性，可以单独查询
    参考开发文档页面：https://partner.tiktokshop.com/docv2/page/650a0483c16ffe02b8dfc80a?external_id=650a0483c16ffe02b8dfc80a
    :return:
    """
    if "keyword" in request.args:
        keyword = request.args.get("keyword")
        return get_attribuets(keyword)
    elif "id" in request.args:
        parent_id = str(request.args.get("id"))
        logging.info(f"id: {parent_id}")
        return get_attribuets("", parent_id)


@app.route("/attr_global", methods=['GET'])
def get_global_attr():
    return get_global_attributes()


@app.route("/1688/commodity_msg", methods=['POST'])
def get_1688_commodity_msg_detail():
    """
    获取1688单独页面的商品数据
    :return:
    """
    data = request.get_json()
    # 阻塞时间是10s
    logging.info(f"get_1688_commodity_msg_detail {json.dumps(data)}")
    global_obj.task_queue.put(data, block=True, timeout=10)
    response = {
        "status": "success",
        "message": "Data synced successfully!"
    }
    return jsonify(response)  # 返回 JSON 响应


@app.route("/resign", methods=['GET'])
def get_auth_code():
    """
    有用户注册之后跳转的三方链接，通过解析参数获取到auth_code，然后申请token
    :return:
    """
    app_key = request.args.get("app_key")
    code = request.args.get("code")
    # 注册信息写入到数据库当中
    result = create_user_token_and_save(app_key, code)
    if result == "fail":
        return send_from_directory('html', 'fail_resign.html')
    return send_from_directory('html', 'success_resign.html')


@app.route("/", methods=["GET"])
def push_trans_title_html():
    """
    :return:
    """
    return send_from_directory('html', 'trans.html')


# result_execl = ''
@app.route('/', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "文件上传失败"}), 400
    file1 = request.files['file1']
    file2 = request.files['file2']
    language = request.form['language']

    global_data = pd.read_excel(file1, sheet_name="Template")
    location_data = pd.read_excel(file2, sheet_name="Template")

    trans_title.trans_parent(global_data, location_data, language)
    # print(res)
    # global result_execl
    # result_execl = result_exce
    response = {
        "status": "success",
        "message": "Data synced successfully!"
    }
    # return send_file(result_exce, as_attachment=True, download_name='data.xlsx',
    #                  mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return response
    # return jsonify(response)  # 返回 JSON 响应
# @app.route('/download/<filename>', methods=['GET'])
# def download_file():
#     return send_file(result_execl, as_attachment=True)


# 运行应用
if __name__ == '__main':
    # global_obj.init_global_conf()
    # 刷新token线程启动
    # if global_obj.production_conf['tk_util']['refresh_token'] == 'true' or global_obj.production_conf['tk_util']['refresh_token'] is True:
    #     global_obj.executor.submit(token_refresh)
    # port = global_obj.global_config['service']['port']
    # host = global_obj.global_config['service']['host']
    # 启动抓取平台的数据写入到队列之后，其他线程消费，避免数据处理导致任务变慢
    # global_obj.executor.submit(data_1688_parse)
    app.run(host="127.0.0.1", port=5000, debug=True)
