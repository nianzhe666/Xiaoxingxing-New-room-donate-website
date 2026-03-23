import requests
import json
import time
import hashlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from config import WECHAT_PAY_CONFIG

class WeChatPay:
    def __init__(self):
        self.mchid = WECHAT_PAY_CONFIG['mchid']
        self.appid = WECHAT_PAY_CONFIG['appid']
        self.private_key_path = WECHAT_PAY_CONFIG['private_key_path']
        self.cert_serial_no = WECHAT_PAY_CONFIG['cert_serial_no']
        self.apiv3_key = WECHAT_PAY_CONFIG['apiv3_key']
        self.notify_url = WECHAT_PAY_CONFIG['notify_url']
        self.return_url = WECHAT_PAY_CONFIG['return_url']
        self.private_key = self._load_private_key()
    
    def _load_private_key(self):
        """加载私钥"""
        with open(self.private_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        return private_key
    
    def _generate_signature(self, method, url, timestamp, nonce_str, body):
        """生成签名"""
        # 构建签名字符串
        message = f"{method}\n{url}\n{timestamp}\n{nonce_str}\n{body}\n"
        # 使用私钥签名
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        # base64编码
        return base64.b64encode(signature).decode('utf-8')
    
    def _get_authorization(self, method, url, body):
        """获取授权头"""
        timestamp = str(int(time.time()))
        nonce_str = hashlib.md5(timestamp.encode()).hexdigest()
        signature = self._generate_signature(method, url, timestamp, nonce_str, body)
        authorization = f"WECHATPAY2-SHA256-RSA2048 mchid={self.mchid},nonce_str={nonce_str},signature={signature},timestamp={timestamp},serial_no={self.cert_serial_no}"
        return authorization
    
    def create_jsapi_payment(self, description, out_trade_no, total, openid):
        """创建JSAPI支付"""
        url = "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi"
        body = json.dumps({
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": self.notify_url,
            "amount": {
                "total": total,
                "currency": "CNY"
            },
            "payer": {
                "openid": openid
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_authorization("POST", "/v3/pay/transactions/jsapi", body)
        }
        response = requests.post(url, headers=headers, data=body)
        return response.json()
    
    def create_native_payment(self, description, out_trade_no, total):
        """创建Native支付"""
        url = "https://api.mch.weixin.qq.com/v3/pay/transactions/native"
        body = json.dumps({
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": self.notify_url,
            "amount": {
                "total": total,
                "currency": "CNY"
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_authorization("POST", "/v3/pay/transactions/native", body)
        }
        response = requests.post(url, headers=headers, data=body)
        return response.json()
    
    def query_order(self, out_trade_no):
        """查询订单"""
        url = f"https://api.mch.weixin.qq.com/v3/pay/transactions/out-trade-no/{out_trade_no}"
        headers = {
            "Authorization": self._get_authorization("GET", f"/v3/pay/transactions/out-trade-no/{out_trade_no}", "")
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def close_order(self, out_trade_no):
        """关闭订单"""
        url = f"https://api.mch.weixin.qq.com/v3/pay/transactions/out-trade-no/{out_trade_no}/close"
        body = json.dumps({})
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_authorization("POST", f"/v3/pay/transactions/out-trade-no/{out_trade_no}/close", body)
        }
        response = requests.post(url, headers=headers, data=body)
        return response.json()
    
    def verify_notification(self, headers, body):
        """验证支付通知"""
        # 实现微信支付通知验证逻辑
        pass
