import logging
import threading
import websocket
import json
import ssl

is_connection_closed = False  # 新增标志位
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_ping(ws):
    """
    每 50 秒发送一次 ping 消息
    :param ws: WebSocket 客户端实例
    """
    global is_connection_closed
    while not is_connection_closed:
        try:
            # 检查连接是否打开
            if ws.sock and ws.sock.connected:
                # 发送 ping 消息
                ws.send(json.dumps({"action": "ping"}))
                logging.info("发送 ping 消息")
            # 等待 25 秒
            threading.Event().wait(25)
        except websocket.WebSocketConnectionClosedException:
            logging.info("连接已关闭，停止发送 ping 消息")
            is_connection_closed = True
            break
        except Exception as e:
            logging.info(f"发送 ping 消息时出错: {e}")

def send_wss_message(wss_url, message):
    """
    封装 WebSocket 连接和消息发送逻辑
    :param wss_url: WebSocket 连接地址
    :param message: 要发送的消息
    """
    def on_open(ws):
        global is_connection_closed
        is_connection_closed = False  # 连接打开时重置标志位
        logging.info("WebSocket 连接已打开")
        ws.send(json.dumps(message))
        # 启动定时发送 ping 消息的线程
        ping_thread = threading.Thread(target=send_ping, args=(ws,))
        ping_thread.daemon = True
        ping_thread.start()

    def on_message(ws, msg):
        logging.info(f"收到消息: {msg}")

    def on_error(ws, err):
        logging.info(f"发生错误: {err}")

    def on_close(ws, close_status_code, close_msg):
        global is_connection_closed
        is_connection_closed = True  # 连接关闭时设置标志位
        logging.info("WebSocket 连接已关闭，尝试重新连接...")
        # 重新调用 send_wss_message 函数进行重连，传入完整参数
        threading.Thread(target=send_wss_message, args=(wss_url, message)).start()

    ws = websocket.WebSocketApp(wss_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
    # 只需要关注要发送的消息
    message_to_send = {
        "sub": "subSymbol",
        "symbol": "BTC_USDT"
    }
    wss_url = "wss://open.icsotic.com/spot/v1/ws/socket"

    send_wss_message(wss_url, message_to_send)