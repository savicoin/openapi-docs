import logging
import time
import uuid

from savicoin.lib.authentication import gen_Signature
from savicoin.lib.request_utils import send_request


def get_order_history(url, method:str,api_Access, api_secret, get_order_details_params, current_milliseconds):
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
    base_api_url = "https://openapi-k.tbbit.xyz"
    accessKey = "your-access-key"
    secretKey = "your-secret-key"

    current_milliseconds = str(int(time.time() * 1000))

    api_url = base_api_url + "/spot/v1/u/trade/order/history"

    get_order_history_params = {
        "symbol": "BTC_USDT",
        # "startTime": 1744373221106, #2025-04-11 20:07:01
        # "endTime": 1745237221000, #2025-04-15 10:00:52
        # "balanceType": "1",
        # "id": 482370252425324032,
        # "direction": "PREV",
        "limit": "10",

    }
    get_order_history(api_url, "GET",accessKey, secretKey, get_order_history_params, current_milliseconds)
