from flask_sqlalchemy import SQLAlchemy

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 物品模型
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.String(50))
    image = db.Column(db.String(255))
    qrcode = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    donated = db.Column(db.Boolean, default=False)
    donor_name = db.Column(db.String(255))
    donor_avatar = db.Column(db.String(255))

# 捐助记录模型
class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item_name = db.Column(db.String(255), nullable=False)
    donor_name = db.Column(db.String(255), nullable=False)
    donor_avatar = db.Column(db.String(255))
    donation_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text)

# 联系信息模型
class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(255))

# 头部图片模型
class Header(db.Model):
    __tablename__ = 'header'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(255))

# 设置模型
class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    default_avatar = db.Column(db.String(255))

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))
