# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : get_sign_from_url.py
@Author   :wangmaosheng
@Date     : 2025/2/4 22:00
@Desc:    : tiktok获取数据的时候会进行身份验证，需要将请求url进行计算进行获取，本类主要存放解析的逻辑相关信息
            tk后台的token相关的信息了，包含token的获取，url传入的参数解码和编码等信息，以及token鉴权、续签等功能，
            未过期的token存放在数据库当中，每次和电商后台交互的时候进行获取
"""
import hmac
import hashlib
from urllib.parse import urlparse, parse_qs


def generate_signature(request, secret):
    # 获取 URL 和查询参数
    url = request.url
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # 提取所有查询参数，排除 sign 和 access_token
    parameter_name_list = [key for key in query_params if key not in ['sign', 'access_token']]

    # 按照字母顺序排序参数名
    parameter_name_list.sort()

    # 拼接请求路径
    parameter_str = parsed_url.path

    for parameter_name in parameter_name_list:
        # 拼接所有参数，格式为 {key}{value}
        parameter_str += parameter_name + ''.join(query_params[parameter_name])

    exap_request = request.prepare()
    # 如果请求的 Content-Type 不是 multipart/form-data，追加请求体
    content_type = request.headers.get("Content-Type")
    if content_type is None:
        content_type = request.headers.get("content-type")
    if content_type and "multipart/form-data" not in content_type.lower():
        try:
            body = exap_request.body
            if body:
                print(f"body: {body}")
                parameter_str += exap_request.body.decode('utf-8')  # 将请求体转为字符串追加
        except Exception as e:
            raise RuntimeError("failed to generate signature params") from e

    # 使用 App secret 包裹拼接的字符串
    signature_params = secret + parameter_str + secret
    # 使用 HMAC-SHA256 生成签名
    return generate_sha256(signature_params, secret)


def generate_sha256(signature_params, secret):
    try:
        # 使用 HMAC-SHA256 算法进行签名
        secret_bytes = secret.encode('utf-8')
        signature_params_bytes = signature_params.encode('utf-8')

        hmac_sha256 = hmac.new(secret_bytes, signature_params_bytes, hashlib.sha256)

        # 获取签名并转换为十六进制字符串
        hash_bytes = hmac_sha256.digest()
        return ''.join(f'{byte:02x}' for byte in hash_bytes)
    except Exception as e:
        raise RuntimeError("failed to generate signature result") from e