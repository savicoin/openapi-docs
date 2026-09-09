import logging
import time

from savicoin.lib.request_utils import send_request


def get_spot_marketing_time(url, method: str):
    logging.info("当前时间:%s",  str(int(time.time() * 1000)))
    resp_json = send_request(method, url,None,None)
    return resp_json


if __name__ == '__main__':
    # 获取系统时间接口
    base_api_url = "https://open.icsotic.com"
    api_url = base_api_url + "/spot/v1/p/time"
    resp_json=get_spot_marketing_time(api_url, "GET")
    assert resp_json["code"] == 0
    assert resp_json["msg"] == "success"
    assert resp_json["data"] is not None
