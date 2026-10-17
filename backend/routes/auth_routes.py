from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User, AuditLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'message': 'Username, Email, dan Password wajib diisi!'}), 400

    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Username atau Email sudah terdaftar!'}), 409

    hashed_password = generate_password_hash(data['password'])
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        nama_lengkap=data.get('nama_lengkap', ''),
        no_telepon=data.get('no_telepon', ''),
        alamat=data.get('alamat', ''),
        role_id=4  # Default: Customer
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registrasi berhasil! Silakan login.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'message': 'Username atau password salah'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role_id})
    
    # Catat log audit SOC
    log = AuditLog(user_id=user.id, aksi='LOGIN_SUCCESS', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()

    return jsonify({'token': access_token, 'role_id': user.role_id}), 200