import time
import logging

from savicoin.lib.authentication import getWssAutoTokenByApi, hmac_sha256, sort_params
from savicoin.lib.wss_connect import send_wss_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def user_data_subscription(wss_url, AccessKey, secretKey, getTokenUrl, current_milliseconds, message_to_send):
    """
    订阅用户数据
    :param wss_url:wss地址
    :param AccessKey:
    :param secretKey:
    :param getTokenUrl:获取token的url
    :param current_milliseconds:
    :param message_to_send: 要发送的消息
    """

    logging.info("当前时间:%s", current_milliseconds)
    add_variable = {
        "timestamp": current_milliseconds
    }
    headers = {"X-Access-Key": AccessKey, "X-Signature": hmac_sha256(secretKey.encode('utf-8'),
                                                                     ("&" + sort_params(add_variable)).encode('utf-8')),
               "X-Request-Timestamp": current_milliseconds,
               "X-Request-Nonce": current_milliseconds}

    currentToken = getWssAutoTokenByApi(getTokenUrl, headers)
    logging.info("获取到的token:%s ", currentToken)
    message_to_send['token'] = currentToken
    logging.info("发送的消息:%s ", message_to_send)
    send_wss_message(wss_url, message_to_send)


if __name__ == '__main__':
    AccessKey = "your-access-key"
    secretKey = "your-secret-key"
    getTokenUrl = "https://openapi-k.tbbit.xyz/spot/v1/u/ws/token"
    wss_url = "wss://openapi-k.tbbit.xyz/spot/v1/ws/socket"

    current_milliseconds = str(int(time.time() * 1000))
    message_to_send = {
        "sub": "subUser",
        "token": None
    }

    user_data_subscription(wss_url, AccessKey, secretKey, getTokenUrl, current_milliseconds, message_to_send)
