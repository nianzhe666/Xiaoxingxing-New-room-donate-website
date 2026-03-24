# 微信支付配置
WECHAT_PAY_CONFIG = {
    # 商户号
    'mchid': 'your_mchid',
    # 应用ID
    'appid': 'your_appid',
    # API证书私钥路径
    'private_key_path': 'path/to/apiclient_key.pem',
    # API证书序列号
    'cert_serial_no': 'your_cert_serial_no',
    # APIv3密钥
    'apiv3_key': 'your_apiv3_key',
    # 回调地址
    'notify_url': 'http://your-domain.com/wechat/notify',
    # 支付成功后跳转地址
    'return_url': 'http://your-domain.com/pay/success'
}

# 小程序配置
MINIPROGRAM_CONFIG = {
    # 小程序AppID
    'appid': 'your_miniprogram_appid',
    # 小程序AppSecret
    'appsecret': 'your_miniprogram_appsecret'
}

# 数据库配置
DATABASE_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///donate_website.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}
