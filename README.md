# 公益捐助平台

## 项目简介

这是一个公益捐助平台，支持物品募捐和微信支付功能，包括网站和微信小程序两个部分。

## 项目结构

```
donate-website-new/
├── app.py                # Flask应用主文件
├── config.py             # 配置文件
├── wechat_pay.py         # 微信支付核心逻辑
├── items.json            # 物品数据文件
├── contact.json          # 联系信息数据文件
├── header.json           # 头部图片数据文件
├── static/               # 静态文件目录
│   ├── css/              # CSS文件
│   └── images/           # 图片文件
├── templates/            # 模板文件
│   ├── index.html        # 首页模板
│   ├── item.html         # 物品详情模板
│   ├── admin.html        # 后台管理模板
│   ├── admin_login.html  # 后台登录模板
│   ├── pay_success.html  # 支付成功模板
│   └── pay_fail.html     # 支付失败模板
└── miniprogram/          # 微信小程序目录
    ├── app.json          # 小程序配置文件
    ├── app.js            # 小程序主文件
    ├── app.wxss          # 小程序全局样式
    └── pages/            # 小程序页面目录
        ├── index/        # 首页
        └── detail/       # 物品详情页
```

## 环境要求

- Python 3.6+
- Flask
- requests
- cryptography

## 安装依赖

```bash
pip install flask requests cryptography
```

## 配置说明

1. **微信支付配置**

   编辑 `config.py` 文件，填写以下参数：

   ```python
   WECHAT_PAY_CONFIG = {
       'mchid': 'your_mchid',  # 商户号
       'appid': 'your_appid',  # 应用ID
       'private_key_path': 'path/to/apiclient_key.pem',  # API证书私钥路径
       'cert_serial_no': 'your_cert_serial_no',  # API证书序列号
       'apiv3_key': 'your_apiv3_key',  # APIv3密钥
       'notify_url': 'http://your-domain.com/wechat/notify',  # 回调地址
       'return_url': 'http://your-domain.com/pay/success'  # 支付成功后跳转地址
   }
   ```

2. **小程序配置**

   编辑 `config.py` 文件，填写以下参数：

   ```python
   MINIPROGRAM_CONFIG = {
       'appid': 'your_miniprogram_appid',  # 小程序AppID
       'appsecret': 'your_miniprogram_appsecret'  # 小程序AppSecret
   }
   ```

## 运行项目

```bash
python app.py
```

项目将在 `http://localhost:5000` 上运行。

## 微信小程序使用说明

1. **导入小程序**

   在微信开发者工具中，选择「导入项目」，选择 `miniprogram` 目录。

2. **配置小程序**

   在 `app.js` 文件中，修改以下代码中的域名：

   ```javascript
   wx.request({
     url: 'https://your-domain.com/api/get_openid',
     // ...
   });
   ```

   在 `pages/index/index.js` 和 `pages/detail/detail.js` 文件中，修改以下代码中的域名：

   ```javascript
   wx.request({
     url: 'https://your-domain.com/api/items',
     // ...
   });
   ```

3. **预览和发布**

   在微信开发者工具中，点击「预览」按钮，使用微信扫码预览小程序。

   发布前，需要在微信公众平台中配置服务器域名，将 `your-domain.com` 添加到「request合法域名」中。

## 微信支付使用流程

1. **网站支付流程**

   - 访问网站首页，浏览需要捐助的物品
   - 点击「查看详情」进入物品详情页
   - 点击「微信支付」按钮
   - 扫描弹出的二维码进行支付
   - 支付成功后，物品状态会更新为「已捐赠」

2. **小程序支付流程**

   - 打开微信小程序
   - 在首页浏览需要捐助的物品
   - 点击「查看详情」进入物品详情页
   - 点击「微信支付」按钮
   - 确认支付信息并完成支付
   - 支付成功后，物品状态会更新为「已捐赠」

## 后台管理

1. **登录后台**

   访问 `http://localhost:5000/admin`，使用以下默认账号登录：
   - 用户名：admin
   - 密码：admin123

2. **管理物品**

   - 添加物品：点击「添加物品」按钮，填写物品信息并上传图片和二维码
   - 编辑物品：点击「编辑」按钮，修改物品信息
   - 删除物品：点击「删除」按钮，删除物品
   - 标记为已捐赠：点击「标记为已捐赠」按钮，填写捐助人信息并上传头像

3. **更新联系信息**

   - 点击「更新联系我们」按钮，上传联系信息图片

4. **更新头部图片**

   - 点击「更新头部图片」按钮，上传头部图片

## API接口说明

1. **获取物品列表**

   ```
   GET /api/items
   ```

   返回值：
   ```json
   {
     "code": 200,
     "data": [
       {
         "id": 1,
         "name": "物品名称",
         "description": "物品描述",
         "price": "100",
         "image": "images/item_1.jpg",
         "qrcode": "images/qrcode_1.jpg",
         "donated": false
       }
     ]
   }
   ```

2. **获取物品详情**

   ```
   GET /api/item/{item_id}
   ```

   返回值：
   ```json
   {
     "code": 200,
     "data": {
       "id": 1,
       "name": "物品名称",
       "description": "物品描述",
       "price": "100",
       "image": "images/item_1.jpg",
       "qrcode": "images/qrcode_1.jpg",
       "donated": false
     }
   }
   ```

3. **获取联系信息**

   ```
   GET /api/contact
   ```

   返回值：
   ```json
   {
     "code": 200,
     "data": {
       "image": "images/contact.jpg"
     }
   }
   ```

4. **获取openid**

   ```
   GET /api/get_openid?code={code}
   ```

   返回值：
   ```json
   {
     "code": 200,
     "openid": "oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"
   }
   ```

5. **创建支付订单**

   ```
   POST /api/create_payment
   Content-Type: application/json
   ```

   请求体：
   ```json
   {
     "item_id": 1,
     "openid": "oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"
   }
   ```

   返回值：
   ```json
   {
     "code": 200,
     "data": {
       "prepay_id": "wx2026032314567890123456789012345678",
       "timeStamp": "1679563000",
       "nonceStr": "abcdefghijklmnopqrstuvwxyz",
       "paySign": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
     }
   }
   ```

## 注意事项

1. **微信支付配置**

   - 需要在微信支付商户平台中获取商户号、应用ID、API证书私钥、API证书序列号和APIv3密钥
   - 需要配置回调地址，确保能被微信服务器访问

2. **小程序配置**

   - 需要在微信公众平台中注册小程序并获取AppID和AppSecret
   - 需要配置服务器域名，将网站域名添加到「request合法域名」中

3. **安全注意事项**

   - 不要将API密钥和证书私钥暴露在代码中
   - 建议使用环境变量或配置文件管理敏感信息
   - 定期更新API密钥和证书

4. **性能优化**

   - 小程序中使用了缓存机制减少网络请求
   - 建议在生产环境中启用CDN加速静态资源
   - 定期清理缓存，避免缓存占用过多存储空间

## 故障排查

1. **支付失败**

   - 检查微信支付配置是否正确
   - 检查网络连接是否正常
   - 检查回调地址是否可访问

2. **小程序无法获取数据**

   - 检查服务器域名配置是否正确
   - 检查API接口是否正常响应
   - 检查网络连接是否正常

3. **图片上传失败**

   - 检查文件权限是否正确
   - 检查存储空间是否充足
   - 检查图片格式是否支持

## 版本更新

- v1.0.0：初始版本，支持物品募捐和微信支付功能
# Xiaoxingxing-New-room-donate-website
