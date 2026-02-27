"""
Flask API Backend for React Frontend
This file converts the Flask app to serve as a REST API
"""
from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import hashlib
import joblib
import pandas as pd
import io
import base64
import json
from datetime import datetime

from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import pyotp
import qrcode

from crypto_utils import generate_keys, sign_data, verify_signature
from zkp_utils import pedersen_commit, point_to_bytes, prove_pedersen_opening, verify_pedersen_opening
from encryption_utils import encrypt_data, decrypt_data
from database import db, Application, Admin, User
from blind_signature_utils import generate_blind_keys, blind_message, sign_blinded_message, unblind_signature

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///privyloans.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Load ML Model
try:
    loan_approval_model = joblib.load('loan_model.joblib')
    scaler = joblib.load('scaler.joblib')
except Exception:
    loan_approval_model = None
    scaler = None

# Crypto Keys
private_key, public_key = generate_keys()
BLIND_KEYS = generate_blind_keys()
BLIND_PUB_N = BLIND_KEYS['N']
BLIND_PUB_E = BLIND_KEYS['e']
BLIND_PRIV_N = BLIND_KEYS['N']
BLIND_PRIV_D = BLIND_KEYS['d']


@login_manager.user_loader
def load_user(user_id):
    if session.get('user_type') == 'Admin':
        return Admin.query.get(int(user_id))
    return User.query.get(int(user_id))


def check_eligibility(age, income):
    errors = []
    if not 21 <= age <= 60:
        errors.append("Age must be between 21 and 60.")
    if income < 250000:
        errors.append("Annual income must be at least ₹2,50,000.")
    return errors


def explain_rejection(age, income, amount, term):
    reasons = []
    if age < 21 or age > 60:
        reasons.append("Age is outside the recommended lending range (21–60).")
    if amount > income * 0.5:
        reasons.append("Requested loan amount is high relative to annual income.")
    if term > 60:
        reasons.append("Loan term exceeds recommended maximum of 60 months.")
    if not reasons:
        reasons.append("The ML model predicted high credit risk based on the input factors.")
    return reasons


# ============ AUTH ROUTES ============

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password, blind_N=str(BLIND_PUB_N))

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    session['user_type'] = 'User'

    return jsonify({
        'message': 'Registration successful',
        'user': {'id': new_user.id, 'username': new_user.username, 'type': 'user', 'mfa_enabled': False}
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        session['user_type'] = 'User'

        if user.mfa_enabled:
            session['mfa_pending'] = True
            session['user_id_mfa'] = user.id
            return jsonify({'mfa_required': True}), 200

        return jsonify({
            'message': 'Login successful',
            'user': {'id': user.id, 'username': user.username, 'type': 'user', 'mfa_enabled': user.mfa_enabled}
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/auth/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()

    if admin and bcrypt.check_password_hash(admin.password_hash, password):
        login_user(admin)
        session['user_type'] = 'Admin'

        return jsonify({
            'message': 'Admin login successful',
            'user': {'id': admin.id, 'username': admin.username, 'type': 'admin'}
        }), 200

    return jsonify({'message': 'Invalid admin credentials'}), 401


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def api_me():
    if isinstance(current_user, Admin):
        return jsonify({
            'user': {'id': current_user.id, 'username': current_user.username, 'type': 'admin'}
        }), 200
    else:
        return jsonify({
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'type': 'user',
                'mfa_enabled': current_user.mfa_enabled
            }
        }), 200


# ============ MFA ROUTES ============

@app.route('/api/mfa/setup', methods=['GET', 'POST'])
@login_required
def api_setup_mfa():
    if request.method == 'POST':
        data = request.get_json()
        code = data.get('code')
        totp = pyotp.TOTP(session['mfa_secret'])

        if totp.verify(code):
            current_user.mfa_secret = session['mfa_secret']
            current_user.mfa_enabled = True
            db.session.commit()
            session.pop('mfa_secret', None)
            return jsonify({'message': 'MFA enabled successfully'}), 200

        return jsonify({'message': 'Invalid code'}), 400

    secret = pyotp.random_base32()
    session['mfa_secret'] = secret
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.username, issuer_name="PrivyLoans")

    img = qrcode.make(provisioning_uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return jsonify({'qr_code': qr_code, 'secret': secret}), 200


@app.route('/api/mfa/verify', methods=['POST'])
@login_required
def api_verify_mfa():
    data = request.get_json()
    code = data.get('code')
    user = User.query.get(session.get('user_id_mfa'))

    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(code):
        session.pop('mfa_pending', None)
        session.pop('user_id_mfa', None)
        return jsonify({'message': 'MFA verified'}), 200

    return jsonify({'message': 'Invalid code'}), 400


# ============ APPLICATION ROUTES ============

@app.route('/api/applications', methods=['GET'])
@login_required
def api_get_applications():
    if isinstance(current_user, Admin):
        return jsonify({'message': 'Admins use /api/admin/applications'}), 403

    decrypted_apps = [{
        'id': app.id,
        'amount': app.amount,
        'purpose': decrypt_data(app.encrypted_purpose),
        'status': app.status
    } for app in current_user.applications]

    return jsonify({'applications': decrypted_apps}), 200


@app.route('/api/applications/apply', methods=['POST'])
@login_required
def api_apply():
    data = request.get_json()

    try:
        name = data.get('name')
        email = data.get('email')
        pan = data.get('pan')
        purpose = data.get('purpose')
        phone = data.get('phone', 'MFA Verified')
        age = int(data.get('age'))
        income = int(data.get('income'))
        term = int(data.get('term'))
        amount = int(data.get('amount'))
    except Exception:
        return jsonify({'message': 'Invalid numeric values'}), 400

    errors = check_eligibility(age, income)
    if errors:
        return jsonify({'message': errors[0]}), 400

    app_id = str(uuid.uuid4())

    value_int = int.from_bytes(hashlib.sha256(f"{name}-{amount}".encode()).digest(), "big")
    C_point, v, r = pedersen_commit(value_int)
    commitment_bytes = point_to_bytes(C_point)
    proof = prove_pedersen_opening(C_point, v, r)
    signature = sign_data(private_key, commitment_bytes)

    blinded_int, blind_r = blind_message(commitment_bytes, BLIND_PUB_N, BLIND_PUB_E)

    new_app = Application(
        id=app_id,
        user_id=current_user.id,
        name=name,
        amount=amount,
        encrypted_email=encrypt_data(email),
        encrypted_phone=encrypt_data(phone),
        encrypted_pan=encrypt_data(pan.upper()),
        encrypted_age=encrypt_data(str(age)),
        encrypted_purpose=encrypt_data(purpose),
        encrypted_term=encrypt_data(str(term)),
        encrypted_income=encrypt_data(str(income)),
        signature=signature.hex(),
        commitment=commitment_bytes.hex(),
        proof_t=proof['t'],
        proof_s1=proof['s1'],
        proof_s2=proof['s2'],
        status='PENDING',
        blind_signature=str(blinded_int),
        blinding_factor_r=str(blind_r)
    )

    db.session.add(new_app)
    db.session.commit()

    return jsonify({'message': 'Application submitted', 'app_id': app_id}), 201


@app.route('/api/applications/<app_id>', methods=['GET'])
@login_required
def api_get_application(app_id):
    app_record = Application.query.filter_by(id=app_id, user_id=current_user.id).first()
    if not app_record:
        return jsonify({'message': 'Application not found'}), 404

    commitment_bytes = bytes.fromhex(app_record.commitment)
    signature_bytes = bytes.fromhex(app_record.signature)
    proof = {'t': app_record.proof_t, 's1': app_record.proof_s1, 's2': app_record.proof_s2}

    is_zkp_valid = verify_signature(public_key, commitment_bytes, signature_bytes) and \
                   verify_pedersen_opening(app_record.commitment, proof)

    data = {
        'id': app_record.id,
        'name': app_record.name,
        'amount': app_record.amount,
        'email': decrypt_data(app_record.encrypted_email),
        'phone': decrypt_data(app_record.encrypted_phone),
        'pan': decrypt_data(app_record.encrypted_pan),
        'age': decrypt_data(app_record.encrypted_age),
        'purpose': decrypt_data(app_record.encrypted_purpose),
        'term': decrypt_data(app_record.encrypted_term),
        'income': decrypt_data(app_record.encrypted_income),
        'status': app_record.status,
        'is_zkp_valid': is_zkp_valid
    }

    return jsonify({'application': data}), 200


@app.route('/api/applications/<app_id>/withdraw', methods=['POST'])
@login_required
def api_withdraw_application(app_id):
    app_record = Application.query.filter_by(id=app_id, user_id=current_user.id).first()
    if not app_record:
        return jsonify({'message': 'Application not found'}), 404

    if app_record.status in ['APPROVED', 'REJECTED']:
        return jsonify({'message': 'Cannot withdraw finalized application'}), 400

    db.session.delete(app_record)
    db.session.commit()
    return jsonify({'message': 'Application withdrawn'}), 200


@app.route('/api/applications/<app_id>/certificate', methods=['GET'])
@login_required
def api_get_certificate(app_id):
    app_record = Application.query.filter_by(id=app_id, user_id=current_user.id).first()
    if not app_record:
        return jsonify({'message': 'Application not found'}), 404

    if app_record.status != 'APPROVED':
        return jsonify({'message': 'Certificate available only for approved applications'}), 400

    try:
        signed_blinded_int = int(app_record.blind_signature)
        r = int(app_record.blinding_factor_r)
        N_user = int(current_user.blind_N)

        token_hex = unblind_signature(signed_blinded_int, r, N_user)

        qr_payload = {
            "app_id": app_record.id,
            "commitment": app_record.commitment,
            "token": token_hex,
            "N": str(BLIND_PUB_N),
            "e": str(BLIND_PUB_E),
        }
        qr_json = json.dumps(qr_payload, separators=(",", ":"))

        img = qrcode.make(qr_json)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

        return jsonify({
            'app_id': app_record.id,
            'commitment': app_record.commitment,
            'token': token_hex,
            'N': str(BLIND_PUB_N),
            'e': str(BLIND_PUB_E),
            'issued_at': datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            'qr_code': qr_code_b64
        }), 200

    except Exception as e:
        return jsonify({'message': f'Could not generate certificate: {str(e)}'}), 500


# ============ ADMIN ROUTES ============

@app.route('/api/admin/applications', methods=['GET'])
@login_required
def api_admin_applications():
    if not isinstance(current_user, Admin):
        return jsonify({'message': 'Admin access required'}), 403

    apps = Application.query.all()
    apps_data = []

    for app_record in apps:
        commitment_bytes = bytes.fromhex(app_record.commitment)
        signature_bytes = bytes.fromhex(app_record.signature)
        proof = {'t': app_record.proof_t, 's1': app_record.proof_s1, 's2': app_record.proof_s2}

        is_valid = verify_signature(public_key, commitment_bytes, signature_bytes) and \
                   verify_pedersen_opening(app_record.commitment, proof)

        prediction = app_record.status.replace("_", " ")
        explanations = []

        if app_record.status == 'PENDING' and loan_approval_model is not None:
            try:
                age = int(decrypt_data(app_record.encrypted_age))
                income = int(decrypt_data(app_record.encrypted_income))
                term = int(decrypt_data(app_record.encrypted_term))
                amount = app_record.amount

                df = pd.DataFrame({
                    'Age': [age],
                    'Income': [income],
                    'Credit_Score': [750],
                    'Loan_Amount': [amount],
                    'Loan_Term': [term],
                    'Employment_Status_Unemployed': [0]
                })

                features = df[['Age', 'Income', 'Credit_Score', 'Loan_Amount', 'Loan_Term', 'Employment_Status_Unemployed']]
                features_scaled = scaler.transform(features) if scaler else features
                result = loan_approval_model.predict(features_scaled)[0]

                if result == 1:
                    app_record.status = 'APPROVED'
                    prediction = "Approved"
                    blinded_int = int(app_record.blind_signature)
                    signed_blinded = sign_blinded_message(blinded_int, int(current_user.blind_priv_N), int(current_user.blind_priv_d))
                    app_record.blind_signature = str(signed_blinded)
                else:
                    app_record.status = 'REJECTED'
                    prediction = "Rejected"
                    explanations = explain_rejection(age, income, amount, term)

                db.session.commit()
            except Exception:
                prediction = "Error"

        apps_data.append({
            "id": app_record.id,
            "name": app_record.name,
            "amount": app_record.amount,
            "valid": is_valid,
            "prediction": prediction,
            "status": app_record.status,
            "explanations": explanations
        })

    return jsonify({'applications': apps_data}), 200


# ============ PUBLIC STATUS CHECK ============

@app.route('/api/status/check', methods=['POST'])
def api_check_status():
    data = request.get_json()
    app_id = data.get('app_id')

    app_record = Application.query.get(app_id)
    if not app_record:
        return jsonify({'message': 'Application not found'}), 404

    commitment_bytes = bytes.fromhex(app_record.commitment)
    signature_bytes = bytes.fromhex(app_record.signature)
    proof = {'t': app_record.proof_t, 's1': app_record.proof_s1, 's2': app_record.proof_s2}

    is_valid = verify_signature(public_key, commitment_bytes, signature_bytes) and \
               verify_pedersen_opening(app_record.commitment, proof)

    return jsonify({
        'application': {
            'name': app_record.name,
            'status': app_record.status,
            'valid': is_valid
        }
    }), 200


# ============ SERVE REACT APP ============

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
