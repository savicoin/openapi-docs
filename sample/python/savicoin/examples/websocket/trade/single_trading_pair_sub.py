import time
import logging

from savicoin.lib.authentication import getWssAutoTokenByApi, hmac_sha256, sort_params
from savicoin.lib.wss_connect import send_wss_message


def user_data_subscription(wss_url, message_to_send):
    """
    5.1.3 统计数据订阅
    :param wss_url:wss地址
    :param message_to_send: 要发送的消息
    """
    logging.info("发送的消息:%s ", message_to_send)
    send_wss_message(wss_url, message_to_send)


if __name__ == '__main__':
    # 5.1.3 统计数据订阅
    wss_url = "wss://openapi-k.tbbit.xyz/spot/v1/ws/socket"
    message_to_send = {
        "sub": "subSymbol",
        "symbol": "BTC_USDT",
    }
    user_data_subscription(wss_url, message_to_send)
