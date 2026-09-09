import logging
import requests

# 创建一个独立的日志器
logger = logging.getLogger('request_utils_logger')
# 避免日志传播到父日志器
logger.propagate = False
# 设置日志级别为 INFO
logger.setLevel(logging.INFO)

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
# 设置控制台处理器的日志级别为 INFO
console_handler.setLevel(logging.INFO)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 将格式器添加到控制台处理器
console_handler.setFormatter(formatter)

# 将控制台处理器添加到日志器
logger.addHandler(console_handler)


def send_request(method, url, headers, params):
    """
    封装公共的 HTTP 请求逻辑并记录日志。

    :param method: HTTP 请求方法，如 'GET', 'POST' 等
    :param url: 请求的 URL
    :param headers: 请求头
    :param params: 请求参数
    :return: 响应的 JSON 数据，如果出错则返回 None
    """
    logger.info("Request url:%s", url)
    logger.info("Request headers:%s", headers)
    logger.info("Request params:%s", params)
    try:
        request_obj = requests.Request(method, url, headers=headers, params=params)
        prepared = request_obj.prepare()
        with requests.Session() as session:
            responses = session.send(prepared)
            if responses.text:
                logger.info(responses.text)
            else:
                logger.info("响应内容为空")
        responses.raise_for_status()
        return responses.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP 错误发生: %s", http_err)
        logger.error("错误响应内容: %s", responses.text if 'responses' in locals() else '')
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error("请求发生错误: %s", req_err)
        return None
    except Exception as e:
        logger.error("发生未知错误: %s", e)
        return None