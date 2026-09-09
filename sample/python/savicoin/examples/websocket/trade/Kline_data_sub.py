import time
import logging

from savicoin.lib.authentication import getWssAutoTokenByApi, hmac_sha256, sort_params
from savicoin.lib.wss_connect import send_wss_message


def kline_data_subscription(wss_url, message_to_send):
    """
    5.1.2 K线数据订阅
    :param wss_url:wss地址
    :param message_to_send: 要发送的消息
    """
    logging.info("发送的消息:%s ", message_to_send)
    send_wss_message(wss_url, message_to_send)


if __name__ == '__main__':
    # 5.1.2 K线数据订阅
    wss_url = "wss://openapi-k.tbbit.xyz/spot/v1/ws/socket"
    message_to_send = {
        "sub": "subKline",
        "symbol": "BTC_USDT",
        "type": "1M" #支持的K线周期：1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M
    }
    kline_data_subscription(wss_url, message_to_send)
