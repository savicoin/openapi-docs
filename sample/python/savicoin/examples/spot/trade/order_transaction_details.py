import logging
import time
import uuid

import requests

from savicoin.lib.authentication import gen_Signature
from savicoin.lib.request_utils import send_request


def get_order_transaction_details(url, method: str, api_Access, api_secret, get_order_details_params,
                                  current_milliseconds):
    logging.info("当前时间:%s", current_milliseconds)

    signature = gen_Signature(api_secret, get_order_details_params, current_milliseconds)
    # 生成随机字符串作为 X-Request-Nonce，防止重放攻击，并取一半长度
    full_nonce = str(uuid.uuid4())
    nonce = full_nonce[:len(full_nonce) // 2]
    Headers = {"X-Access-Key": api_Access, "X-Signature": signature, "X-Request-Timestamp": current_milliseconds,
               "X-Request-Nonce": nonce}
    resp_json = send_request(method, url, Headers, get_order_details_params)
    return resp_json


if __name__ == '__main__':
    base_api_url = "https://open.icsotic.com"
    accessKey = "your-access-key"
    secretKey = "your-secret-key"
    current_milliseconds = str(int(time.time() * 1000))

    api_url = base_api_url + "/spot/v1/u/trade/order/deal"

    get_order_transaction_details_params = {
        # "orderId": "485207109987257600",
        # "symbol": "ETH_USDT",
        "balanceType": 1,
        # "page": "1",
        # "size": "10"
    }
    get_order_transaction_details(api_url,"GET", accessKey, secretKey, get_order_transaction_details_params,
                                  current_milliseconds)
