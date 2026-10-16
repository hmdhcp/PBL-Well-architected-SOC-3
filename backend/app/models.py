from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nama_lengkap = db.Column(db.String(150))
    no_telepon = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nama_produk = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text)
    harga = db.Column(db.Numeric(12, 2), nullable=False)
    stok = db.Column(db.Integer, nullable=False, default=0)
    gambar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_harga = db.Column(db.Numeric(12, 2), nullable=False)
    status_pembayaran = db.Column(db.String(50), default='Pending')
    bukti_pembayaran = db.Column(db.String(255))
    midtrans_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    harga_satuan = db.Column(db.Numeric(12, 2), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    aksi = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45))
    detail = db.Column(db.Text)
    waktu = db.Column(db.DateTime, default=datetime.utcnow)