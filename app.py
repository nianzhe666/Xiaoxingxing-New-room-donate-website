from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import json
import hashlib
import time

app = Flask(__name__)
# 从环境变量读取SECRET_KEY
import os
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 模拟用户数据
users = {
    'user1': {'password': '123456', 'name': '张三', 'avatar': 'images/donor_1.jpg'},
    'user2': {'password': '123456', 'name': '李四', 'avatar': 'images/donor_1.jpg'}
}

# 用户头像存储路径
AVATAR_FOLDER = 'static/images/avatars'

# 确保头像存储目录存在
if not os.path.exists(AVATAR_FOLDER):
    os.makedirs(AVATAR_FOLDER)

# 模拟支付状态
payment_status = {}

# 捐助记录
DONATIONS_FILE = 'donations.json'

# 确保捐助记录文件存在
def ensure_donations_file():
    if not os.path.exists(DONATIONS_FILE):
        with open(DONATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

# 加载捐助记录
def load_donations():
    ensure_donations_file()
    with open(DONATIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存捐助记录
def save_donations(donations):
    with open(DONATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(donations, f, ensure_ascii=False, indent=2)

# 数据存储文件
ITEMS_FILE = 'items.json'
CONTACT_FILE = 'contact.json'
HEADER_FILE = 'header.json'
SETTINGS_FILE = 'settings.json'

# 确保数据文件存在
def ensure_files_exist():
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'image': ''}, f, ensure_ascii=False, indent=2)
    if not os.path.exists(HEADER_FILE):
        with open(HEADER_FILE, 'w', encoding='utf-8') as f:
            json.dump({'image': ''}, f, ensure_ascii=False, indent=2)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'default_avatar': 'images/donor_1.jpg'}, f, ensure_ascii=False, indent=2)

# 加载物品数据
def load_items():
    ensure_files_exist()
    with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存物品数据
def save_items(items):
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

# 加载联系我们数据
def load_contact():
    ensure_files_exist()
    with open(CONTACT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存联系我们数据
def save_contact(contact):
    with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
        json.dump(contact, f, ensure_ascii=False, indent=2)

# 加载头部图片数据
def load_header():
    ensure_files_exist()
    with open(HEADER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存头部图片数据
def save_header(header):
    with open(HEADER_FILE, 'w', encoding='utf-8') as f:
        json.dump(header, f, ensure_ascii=False, indent=2)

# 加载设置数据
def load_settings():
    ensure_files_exist()
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存设置数据
def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# 标记物品为已捐赠
@app.route('/admin/mark_donated/<int:item_id>', methods=['POST'])
def mark_donated(item_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return redirect(url_for('admin_panel'))
    
    item['donated'] = True
    item['donor_name'] = request.form.get('donor_name')
    
    # 处理捐助人头像上传
    donor_avatar = request.files.get('donor_avatar')
    if donor_avatar:
        avatar_filename = f'donor_{item_id}.jpg'
        donor_avatar.save(os.path.join('static/images', avatar_filename))
        item['donor_avatar'] = f'images/{avatar_filename}'
    else:
        # 如果没有上传头像，使用默认头像
        settings = load_settings()
        item['donor_avatar'] = settings.get('default_avatar', 'images/donor_1.jpg')
    
    save_items(items)
    
    # 同步到捐助记录
    donations = load_donations()
    
    # 检查是否已有该物品的捐助记录
    existing_donation = next((d for d in donations if d['item_id'] == item_id), None)
    if not existing_donation:
        # 获取捐赠时间
        donation_time = request.form.get('donation_time')
        if not donation_time:
            # 如果没有设置时间，使用当前时间
            donation_time = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # 转换 datetime-local 格式到标准格式
            donation_time = donation_time.replace('T', ' ')
        
        # 获取留言内容
        message = request.form.get('message', '')
        
        # 添加新的捐助记录
        new_donation = {
            'id': len(donations) + 1,
            'item_id': item['id'],
            'item_name': item['name'],
            'donor_name': item['donor_name'],
            'donor_avatar': item['donor_avatar'],
            'donation_time': donation_time,
            'message': message
        }
        donations.append(new_donation)
        save_donations(donations)
    
    return redirect(url_for('admin_panel'))

# 标记物品为未捐赠
@app.route('/admin/mark_not_donated/<int:item_id>')
def mark_not_donated(item_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return redirect(url_for('admin_panel'))
    
    item['donated'] = False
    item.pop('donor_name', None)
    item.pop('donor_avatar', None)
    
    save_items(items)
    
    # 同步删除相应的捐助记录
    donations = load_donations()
    donations = [d for d in donations if d['item_id'] != item_id]
    save_donations(donations)
    
    return redirect(url_for('admin_panel'))

# 主页
@app.route('/')
def index():
    items = load_items()
    header = load_header()
    donations = load_donations()
    
    # 统计捐助数据
    donors = list(set([d['donor_name'] for d in donations]))
    donated_items = list(set([d['item_id'] for d in donations]))
    
    # 处理捐助人数据，去重并统计次数
    donor_counts = {}
    # 加载设置以获取默认头像
    settings = load_settings()
    default_avatar = settings.get('default_avatar', 'images/donor_1.jpg')
    for donation in donations:
        donor_name = donation['donor_name']
        if donor_name not in donor_counts:
            donor_counts[donor_name] = {
                'count': 0,
                'avatar': donation.get('donor_avatar', default_avatar),
                'donations': []
            }
        donor_counts[donor_name]['count'] += 1
        donor_counts[donor_name]['donations'].append(donation)
    
    # 按捐助次数排序，匿名用户（好心人）放在最前面
    sorted_donors = []
    # 先添加匿名用户
    if '好心人' in donor_counts:
        sorted_donors.append(('好心人', donor_counts['好心人']))
        del donor_counts['好心人']
    # 然后按捐助次数排序
    sorted_donors.extend(sorted(donor_counts.items(), key=lambda x: x[1]['count'], reverse=True))
    
    # 获取最近5位捐助人（去重）
    recent_donors = []
    if donations:
        # 按时间排序，获取最新的5个
        donations.sort(key=lambda x: x['donation_time'], reverse=True)
        recent_donors = donations[:5]
    
    # 检测设备类型
    user_agent = request.headers.get('User-Agent', '')
    device_type = 'desktop'
    if 'Mobile' in user_agent:
        device_type = 'mobile'
    elif 'Tablet' in user_agent:
        device_type = 'tablet'
    
    # 优先显示未募捐的物品，已募捐的物品按捐助时间从晚到早排序
    def get_item_sort_key(item):
        if not item.get('donated', False):
            # 未捐助的物品按创建时间排序，最新的在前
            if 'created_at' in item:
                import datetime
                try:
                    created_time = datetime.datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S')
                    # 返回负数，使时间晚的排在前面
                    return (0, -created_time.timestamp())
                except:
                    return (0, 0)
            else:
                return (0, 0)  # 没有创建时间的排在最后
        else:
            # 已捐助的物品按捐助时间排序
            # 查找对应的捐助记录
            donation = next((d for d in donations if d['item_id'] == item['id']), None)
            if donation and 'donation_time' in donation:
                # 转换时间为可排序的格式
                import datetime
                try:
                    donation_time = datetime.datetime.strptime(donation['donation_time'], '%Y-%m-%d %H:%M:%S')
                    # 返回负数，使时间晚的排在前面
                    return (1, -donation_time.timestamp())
                except:
                    return (1, 0)
            else:
                return (1, 0)
    
    items.sort(key=get_item_sort_key)
    
    return render_template('index.html', items=items, header=header, donations=donations, donors=donors, donated_items=donated_items, recent_donors=recent_donors, sorted_donors=sorted_donors, device_type=device_type)

# 捐助列表页面
@app.route('/donations')
def donations_list():
    donations = load_donations()
    header = load_header()
    
    # 按时间排序，最新的在前
    if donations:
        donations.sort(key=lambda x: x['donation_time'], reverse=True)
    
    return render_template('donations.html', donations=donations, header=header)

# 物品详情页
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return redirect(url_for('index'))
    contact = load_contact()
    header = load_header()
    return render_template('item.html', item=item, contact=contact, header=header)

# 后台管理登录
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # 简单的登录验证，实际项目中应该使用更安全的方式
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
    header = load_header()
    return render_template('admin_login.html', header=header)

# 后台管理面板
@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    items = load_items()
    contact = load_contact()
    header = load_header()
    donations = load_donations()
    settings = load_settings()
    
    # 按创建时间从晚到早排序
    def sort_items_by_created_at(item):
        if 'created_at' in item:
            import datetime
            try:
                created_time = datetime.datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S')
                return -created_time.timestamp()
            except:
                return 0
        else:
            return 0
    
    items.sort(key=sort_items_by_created_at)
    
    return render_template('admin.html', items=items, contact=contact, header=header, donations=donations, users=users, settings=settings, load_settings=load_settings)

# 登出
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))

# 添加物品
@app.route('/admin/add_item', methods=['POST'])
def add_item():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    items = load_items()
    new_id = max([item['id'] for item in items]) + 1 if items else 1
    
    # 处理文件上传
    image = request.files.get('image')
    image_path = None
    if image:
        image_filename = f'item_{new_id}.jpg'
        image.save(os.path.join('static/images', image_filename))
        image_path = f'images/{image_filename}'
    
    new_item = {
        'id': new_id,
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': image_path,
        'qrcode': request.files.get('qrcode').filename if request.files.get('qrcode') else None,
        'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 处理二维码上传
    qrcode = request.files.get('qrcode')
    if qrcode:
        # 保存二维码原图
        qrcode_original_filename = f'qrcode_{new_id}_original.jpg'
        qrcode.save(os.path.join('static/images/original', qrcode_original_filename))
        
        # 保存二维码
        qrcode_filename = f'qrcode_{new_id}.jpg'
        qrcode.save(os.path.join('static/images', qrcode_filename))
        new_item['qrcode'] = f'images/{qrcode_filename}'
    
    items.append(new_item)
    save_items(items)
    return redirect(url_for('admin_panel'))

# 编辑物品
@app.route('/admin/edit_item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return redirect(url_for('admin_panel'))
    
    # 处理文件上传
    image = request.files.get('image')
    if image:
        image_filename = f'item_{item_id}.jpg'
        image.save(os.path.join('static/images', image_filename))
        item['image'] = f'images/{image_filename}'
    
    # 处理二维码上传
    qrcode = request.files.get('qrcode')
    if qrcode:
        # 保存二维码原图
        qrcode_original_filename = f'qrcode_{item_id}_original.jpg'
        qrcode.save(os.path.join('static/images/original', qrcode_original_filename))
        
        # 保存二维码
        qrcode_filename = f'qrcode_{item_id}.jpg'
        qrcode.save(os.path.join('static/images', qrcode_filename))
        item['qrcode'] = f'images/{qrcode_filename}'
    
    # 更新其他字段
    item['name'] = request.form.get('name')
    item['description'] = request.form.get('description')
    item['price'] = request.form.get('price')
    
    save_items(items)
    return redirect(url_for('admin_panel'))

# 删除物品
@app.route('/admin/delete_item/<int:item_id>')
def delete_item(item_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    
    # 同步删除相应的捐助记录
    donations = load_donations()
    donations = [d for d in donations if d['item_id'] != item_id]
    save_donations(donations)
    
    return redirect(url_for('admin_panel'))

# 更新联系我们
@app.route('/admin/update_contact', methods=['POST'])
def update_contact():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    contact = load_contact()
    
    # 处理文件上传
    image = request.files.get('image')
    if image:
        image_filename = 'contact.jpg'
        image.save(os.path.join('static/images', image_filename))
        contact['image'] = f'images/{image_filename}'
    
    save_contact(contact)
    return redirect(url_for('admin_panel'))

# 更新头部图片
@app.route('/admin/update_header', methods=['POST'])
def update_header():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    header = load_header()
    
    # 处理文件上传
    image = request.files.get('image')
    if image:
        image_filename = 'header.jpg'
        image.save(os.path.join('static/images', image_filename))
        header['image'] = f'images/{image_filename}'
    
    save_header(header)
    return redirect(url_for('admin_panel'))

# 更新默认头像
@app.route('/admin/update_default_avatar', methods=['POST'])
def update_default_avatar():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    settings = load_settings()
    
    # 处理文件上传
    image = request.files.get('default_avatar')
    if image:
        image_filename = 'default_avatar.jpg'
        image.save(os.path.join('static/images', image_filename))
        settings['default_avatar'] = f'images/{image_filename}'
    
    save_settings(settings)
    return redirect(url_for('admin_panel'))

# 模拟用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['user_name'] = users[username]['name']
            # 使用用户头像或默认头像
            settings = load_settings()
            session['user_avatar'] = users[username].get('avatar', settings.get('default_avatar', 'images/donor_1.jpg'))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    return render_template('login.html')

# 模拟用户登出
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_name', None)
    session.pop('user_avatar', None)
    return redirect(url_for('index'))

# 模拟创建支付订单
@app.route('/api/create_payment', methods=['POST'])
def create_payment():
    data = request.json
    item_id = data.get('item_id')
    
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return jsonify({'code': 404, 'message': '物品不存在'})
    
    if item.get('donated'):
        return jsonify({'code': 400, 'message': '物品已被捐赠'})
    
    # 生成订单号
    out_trade_no = f"{int(time.time())}_{hashlib.md5(str(item_id).encode()).hexdigest()[:8]}"
    
    # 保存支付状态
    payment_status[out_trade_no] = {
        'item_id': item_id,
        'status': 'pending',
        'create_time': time.time()
    }
    
    # 保存订单信息
    if 'orders' not in session:
        session['orders'] = []
    session['orders'].append({
        'out_trade_no': out_trade_no,
        'item_id': item_id,
        'create_time': time.time(),
        'anonymous': request.json.get('anonymous', False)
    })
    session.modified = True
    
    # 模拟支付参数
    result = {
        'prepay_id': out_trade_no,
        'timeStamp': str(int(time.time())),
        'nonceStr': hashlib.md5(str(time.time()).encode()).hexdigest(),
        'paySign': hashlib.md5((out_trade_no + str(int(time.time()))).encode()).hexdigest()
    }
    
    return jsonify({'code': 200, 'data': result})

# 模拟支付通知
@app.route('/simulate/pay', methods=['POST'])
def simulate_pay():
    out_trade_no = request.form.get('out_trade_no')
    anonymous = request.form.get('anonymous') == 'true'
    if out_trade_no in payment_status:
        payment_status[out_trade_no]['status'] = 'success'
        
        # 标记物品为已捐赠
        order = next((o for o in session.get('orders', []) if o['out_trade_no'] == out_trade_no), None)
        if order:
            items = load_items()
            item = next((item for item in items if item['id'] == order['item_id']), None)
            if item:
                # 处理匿名捐助
                if anonymous:
                    donor_name = '好心人'
                    # 匿名捐助使用特定的头像，与默认头像不同
                    donor_avatar = 'images/anonymous_avatar.jpg'
                    # 保存匿名捐助信息到session
                    session['last_donation_anonymous'] = True
                else:
                    donor_name = session.get('user_name', '匿名用户')
                    # 从设置中获取默认头像
                    settings = load_settings()
                    donor_avatar = session.get('user_avatar', settings.get('default_avatar', 'images/donor_1.jpg'))
                    # 保存非匿名捐助信息到session
                    session['last_donation_anonymous'] = False
                
                item['donated'] = True
                item['donor_name'] = donor_name
                item['donor_avatar'] = donor_avatar
                save_items(items)
                
                # 添加捐助记录
                donations = load_donations()
                new_donation = {
                    'id': len(donations) + 1,
                    'item_id': item['id'],
                    'item_name': item['name'],
                    'donor_name': donor_name,
                    'donor_avatar': donor_avatar,
                    'donation_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'message': ''
                }
                donations.append(new_donation)
                save_donations(donations)
        
        return redirect(url_for('pay_success'))
    else:
        return redirect(url_for('pay_fail'))

# 支付成功
@app.route('/pay/success')
def pay_success():
    return render_template('pay_success.html')

# 支付失败
@app.route('/pay/fail')
def pay_fail():
    return render_template('pay_fail.html')

# 添加留言
@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form.get('message')
    if session.get('user'):
        # 获取最新的捐助记录
        donations = load_donations()
        if donations:
            # 检查是否是匿名捐助
            if session.get('last_donation_anonymous'):
                # 找到最新的匿名捐助记录（好心人）
                user_donations = [d for d in donations if d['donor_name'] == '好心人']
            else:
                # 找到当前用户的最新捐助记录
                user_donations = [d for d in donations if d['donor_name'] == session.get('user_name')]
            
            if user_donations:
                # 按时间排序，获取最新的
                user_donations.sort(key=lambda x: x['donation_time'], reverse=True)
                latest_donation = user_donations[0]
                # 更新留言
                for donation in donations:
                    if donation['id'] == latest_donation['id']:
                        donation['message'] = message
                        break
                save_donations(donations)
                # 清除session中的匿名捐助标记
                session.pop('last_donation_anonymous', None)
    return redirect(url_for('index'))

# 编辑捐助留言
@app.route('/admin/edit_donation_message/<int:donation_id>', methods=['POST'])
def edit_donation_message(donation_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    message = request.form.get('message')
    donor_name = request.form.get('donor_name')
    user_id = request.form.get('user_id')
    
    donations = load_donations()
    for donation in donations:
        if donation['id'] == donation_id:
            # 更新留言
            donation['message'] = message
            
            # 更新捐助人姓名
            if donor_name:
                donation['donor_name'] = donor_name
            
            # 处理头像上传
            donor_avatar = request.files.get('donor_avatar')
            if donor_avatar:
                avatar_filename = f'donor_{donation_id}.jpg'
                donor_avatar.save(os.path.join('static/images', avatar_filename))
                donation['donor_avatar'] = f'images/{avatar_filename}'
            
            # 关联用户
            if user_id and user_id in users:
                donation['donor_name'] = users[user_id]['name']
                # 从设置中获取默认头像
                settings = load_settings()
                donation['donor_avatar'] = users[user_id].get('avatar', settings.get('default_avatar', 'images/donor_1.jpg'))
            
            break
    save_donations(donations)
    
    # 同步更新物品中的捐助人信息
    items = load_items()
    for item in items:
        if item.get('donated') and item.get('donor_name') == donation['donor_name']:
            item['donor_name'] = donation['donor_name']
            item['donor_avatar'] = donation['donor_avatar']
    save_items(items)
    
    return redirect(url_for('admin_panel'))

# 删除捐助记录
@app.route('/admin/delete_donation/<int:donation_id>')
def delete_donation(donation_id):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    donations = load_donations()
    donation_to_delete = None
    
    # 找到要删除的捐助记录
    for donation in donations:
        if donation['id'] == donation_id:
            donation_to_delete = donation
            break
    
    if donation_to_delete:
        # 从捐助记录中删除
        donations = [d for d in donations if d['id'] != donation_id]
        save_donations(donations)
        
        # 同步更新对应物品的募捐状态
        items = load_items()
        for item in items:
            if item.get('donated') and item.get('id') == donation_to_delete['item_id']:
                item['donated'] = False
                item.pop('donor_name', None)
                item.pop('donor_avatar', None)
        save_items(items)
    
    return redirect(url_for('admin_panel'))

# 管理用户页面
@app.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    header = load_header()
    return render_template('admin_users.html', header=header, users=users)

# 编辑用户
@app.route('/admin/edit_user/<username>', methods=['POST'])
def edit_user(username):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    new_username = request.form.get('new_username')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    
    # 处理用户名修改
    if new_username and new_username != username:
        # 创建新用户条目
        users[new_username] = users[username].copy()
        # 删除旧用户条目
        del users[username]
        # 更新用户名变量
        username = new_username
    
    # 处理密码修改
    if new_password:
        users[username]['password'] = new_password
    
    # 处理姓名修改
    if new_name:
        users[username]['name'] = new_name
    
    # 处理头像上传
    avatar = request.files.get('avatar')
    if avatar:
        avatar_filename = f"avatar_{username}.jpg"
        avatar_path = os.path.join(AVATAR_FOLDER, avatar_filename)
        avatar.save(avatar_path)
        users[username]['avatar'] = f"images/avatars/{avatar_filename}"
    
    return redirect(url_for('admin_users'))

# 删除用户
@app.route('/admin/delete_user/<username>')
def delete_user(username):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    if username in users:
        del users[username]
    
    return redirect(url_for('admin_users'))

# 添加用户
@app.route('/admin/add_user', methods=['POST'])
def add_user():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    
    if username and password and name:
        # 从设置中获取默认头像
        settings = load_settings()
        users[username] = {
            'password': password,
            'name': name,
            'avatar': settings.get('default_avatar', 'images/donor_1.jpg')
        }
    
    return redirect(url_for('admin_users'))

# 个人设置页面
@app.route('/settings')
def settings():
    if not session.get('user'):
        return redirect(url_for('login'))
    header = load_header()
    return render_template('settings.html', header=header)

# 同步更新捐助人信息
def sync_donor_info(username, new_name=None, new_avatar=None):
    # 更新捐助记录中的信息
    donations = load_donations()
    for donation in donations:
        if donation['donor_name'] == users[username]['name'] and donation['donor_avatar'] == users[username].get('avatar'):
            if new_name:
                donation['donor_name'] = new_name
            if new_avatar:
                donation['donor_avatar'] = new_avatar
    save_donations(donations)
    
    # 更新物品中的捐助人信息
    items = load_items()
    for item in items:
        if item.get('donor_name') == users[username]['name'] and item.get('donor_avatar') == users[username].get('avatar'):
            if new_name:
                item['donor_name'] = new_name
            if new_avatar:
                item['donor_avatar'] = new_avatar
    save_items(items)

# 更新头像
@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    if not session.get('user'):
        return redirect(url_for('login'))
    
    avatar = request.files.get('avatar')
    if avatar:
        # 保存头像文件
        avatar_filename = f"avatar_{session['user']}.jpg"
        avatar_path = os.path.join(AVATAR_FOLDER, avatar_filename)
        avatar.save(avatar_path)
        
        # 更新用户头像信息
        new_avatar = f"images/avatars/{avatar_filename}"
        users[session['user']]['avatar'] = new_avatar
        session['user_avatar'] = new_avatar
        
        # 同步更新捐助人信息
        sync_donor_info(session['user'], new_avatar=new_avatar)
    
    return redirect(url_for('settings'))

# 更新名字
@app.route('/update_name', methods=['POST'])
def update_name():
    if not session.get('user'):
        return redirect(url_for('login'))
    
    new_name = request.form.get('name')
    if new_name:
        # 更新用户名字信息
        users[session['user']]['name'] = new_name
        session['user_name'] = new_name
        
        # 同步更新捐助人信息
        sync_donor_info(session['user'], new_name=new_name)
    
    return redirect(url_for('settings'))

# API接口：获取物品列表
@app.route('/api/items')
def api_items():
    items = load_items()
    return jsonify({'code': 200, 'data': items})

# API接口：获取物品详情
@app.route('/api/item/<int:item_id>')
def api_item_detail(item_id):
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify({'code': 200, 'data': item})
    else:
        return jsonify({'code': 404, 'message': '物品不存在'})

# API接口：获取联系信息
@app.route('/api/contact')
def api_contact():
    contact = load_contact()
    return jsonify({'code': 200, 'data': contact})

# API接口：获取openid（模拟）
@app.route('/api/get_openid')
def api_get_openid():
    # 模拟返回openid
    return jsonify({'code': 200, 'openid': 'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'})

if __name__ == '__main__':
    # 仅在开发环境中使用
    app.run(debug=False, host='0.0.0.0', port=5000)