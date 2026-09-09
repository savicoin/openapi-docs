import hashlib
import hmac
import time

import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sort_params(params):
    """
    对请求参数按键名字母顺序排序

    :param params: 包含请求参数的字典
    :return: 按键名排序后的参数字符串
    """
    sorted_params = sorted(params.items())
    param_str = '&'.join([f"{key}={value}" for key, value in sorted_params])
    return param_str


def hmac_sha256(api_secret, message):
    """
    使用 HMAC-SHA256 算法计算消息的哈希值
    :param api_secret: 密钥，字节类型
    :param message: 要计算哈希值的消息，字节类型
    :return: 计算得到的 HMAC-SHA256 哈希值，十六进制字符串
    """
    # 创建 HMAC 对象，使用 SHA-256 哈希算法
    h = hmac.new(api_secret, message, hashlib.sha256)
    # 计算哈希值并以十六进制字符串形式返回
    return h.hexdigest()


def gen_Signature(api_secret, payload, milliseconds):
    """
    生成签名信息
    :param milliseconds: milliseconds
    :param api_secret: secretKey
    :param payload: 包含请求参数的字典
    :return: 生成的签名信息
    """
    sorted_param_str = sort_params(payload)
    logging.info("排序后的参数字符串:%s", sorted_param_str)

    ParamsAddTimestamp = sorted_param_str + "&timestamp=" + milliseconds
    logging.info("在参数字符串末尾附加时间戳：%s", ParamsAddTimestamp)

    # 将 SecretKey 和 ParamsAddTimestamp 编码为字节类型入参 获取签名信息
    signature = hmac_sha256(api_secret.encode('utf-8'), ParamsAddTimestamp.encode('utf-8'))
    logging.info("生成的签名信息:%s", signature)
    return signature


def getWssAutoTokenByApi(url, headers):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        logging.info("获取token: %s", data)
        if data['data'] is not None:
            return data['data']
        else:
            logging.error("获取token失败，错误码：%s，错误信息：%s", data['data'], data['message'])
            return None
    else:
        logging.error("请求失败，状态码：%s", resp.status_code)
        return None


if __name__ == '__main__':
    openApiBaseUrl = "https://open.icsotic.com"
    AccessKey = "your-access-key"
    secretKey = "your-secret-key"
    # 定义一个函数用于对请求参数进行排序
    current_milliseconds = str(int(time.time() * 1000))
    logging.info("当前时间:%s", current_milliseconds)
    createOrderParams = {"symbol": "BTC_USDT", "direction": "BUY", "tradeType": "LIMIT",
                         "totalAmount": "1", "price": "100",
                         "balanceType": 1}

    signature = gen_Signature(secretKey, createOrderParams, current_milliseconds)
    Headers = {"X-Access-Key": AccessKey, "X-Signature": signature, "X-Request-Timestamp": current_milliseconds,
               "X-Request-Nonce": current_milliseconds}
    # 创建订单
    createOrderUrl = openApiBaseUrl + "/spot/v1/u/trade/order/create"
    logging.info("Headers:%s", Headers)
    logging.info("body:%s", createOrderParams)
    responses = requests.post(createOrderUrl, headers=Headers, json=createOrderParams)
    logging.info("%s",responses.text)

    # # 获取wss token
    # getTokenUrl = "https://open.icsotic.com/spot/v1/u/ws/token"
    # sendMessage = {
    #     "timestamp": current_milliseconds
    # }
    #
    # headers = {"X-Access-Key": AccessKey, "X-Signature": hmac_sha256(secretKey.encode('utf-8'),
    #                                                                  ("&" + sort_params(sendMessage)).encode('utf-8')),
    #            "X-Request-Timestamp": current_milliseconds,
    #            "X-Request-Nonce": current_milliseconds}
    #
    # currentToken = getWssAutoTokenByApi(getTokenUrl, headers)
    # print(currentToken)
