from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import hashlib
import random
import joblib
import pandas as pd
import io
import base64
import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import pyotp
import qrcode

from crypto_utils import generate_keys, sign_data, verify_signature
from zkp_utils import pedersen_commit, point_to_bytes, prove_pedersen_opening, verify_pedersen_opening
from encryption_utils import encrypt_data, decrypt_data
from database import db, Application, Admin, User
from blind_signature_utils import generate_blind_keys, blind_message, sign_blinded_message, unblind_signature

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///privyloans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# ==========================
# ML MODEL + SCALER LOADING
# ==========================
try:
    loan_approval_model = joblib.load('loan_model.joblib')
    scaler = joblib.load('scaler.joblib')
except Exception:
    loan_approval_model = None
    scaler = None

# ==========================
# CRYPTO KEYS (demo only)
# ==========================
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
        errors.append("Eligibility Error: Age must be between 21 and 60.")
    if income < 250000:
        errors.append("Eligibility Error: Annual income must be at least ₹2,50,000.")
    return errors


# -----------------------------------------
# Transparent explanation for ML rejections
# -----------------------------------------
def explain_rejection(age, income, amount, term):
    """
    Returns a list of human-readable reasons for rejection
    based on simple, transparent rules. This does NOT change
    the ML prediction; it only explains it.
    """
    reasons = []

    # Age rule
    if age < 21 or age > 60:
        reasons.append("Age is outside the recommended lending range (21–60).")

    # Income vs amount rule (very rough: amount should not exceed 50% of annual income)
    if amount > income * 0.5:
        reasons.append("Requested loan amount is high relative to annual income.")

    # Term rule
    if term > 60:
        reasons.append("Loan term exceeds recommended maximum of 60 months.")

    # If no specific rule fired, use a generic ML message
    if not reasons:
        reasons.append("The ML model predicted high credit risk based on the input factors.")

    return reasons


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin'))
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=hashed_password, blind_N=str(BLIND_PUB_N))

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        session['user_type'] = 'User'
        return redirect(url_for('setup_user_mfa'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If an admin is logged in → force logout admin
    if current_user.is_authenticated and isinstance(current_user, Admin):
        logout_user()
        session.clear()

    # If user is already logged in → go to dashboard
    if current_user.is_authenticated and isinstance(current_user, User):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            session['user_type'] = 'User'

            if user.mfa_enabled:
                session['mfa_pending'] = True
                session['user_id_mfa'] = user.id
                return redirect(url_for('verify_user_mfa'))

            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin'))

    if not current_user.mfa_enabled:
        return redirect(url_for('setup_user_mfa'))

    decrypted_apps = [{
        'id': app.id,
        'amount': app.amount,
        'purpose': decrypt_data(app.encrypted_purpose),
        'status': app.status
    } for app in current_user.applications]

    return render_template('dashboard.html', applications=decrypted_apps)


@app.route('/apply/setup-mfa', methods=['GET', 'POST'])
@login_required
def setup_user_mfa():
    if current_user.mfa_enabled:
        return redirect(url_for('apply'))

    user = current_user

    if request.method == 'POST':
        totp = pyotp.TOTP(session['mfa_secret'])
        if totp.verify(request.form.get('mfa_code')):
            user.mfa_secret = session['mfa_secret']
            user.mfa_enabled = True
            db.session.commit()
            session.pop('mfa_secret', None)
            return redirect(url_for('apply'))
        flash("Invalid code.", "danger")
        return redirect(url_for('setup_user_mfa'))

    secret = pyotp.random_base32()
    session['mfa_secret'] = secret
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.username, issuer_name="PrivyLoans")

    img = qrcode.make(provisioning_uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render_template("setup_user_mfa.html", qr_code_image=qr_code)


@app.route('/apply/verify-mfa', methods=['GET', 'POST'])
@login_required
def verify_user_mfa():
    if current_user.mfa_enabled and 'mfa_pending' not in session:
        return redirect(url_for('apply'))

    user = User.query.get(session.get('user_id_mfa'))

    if request.method == 'POST':
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(request.form.get('mfa_code')):
            session.pop('mfa_pending', None)
            session.pop('user_id_mfa', None)
            return redirect(url_for('apply'))
        flash("Invalid code.", "danger")

    return render_template('verify_mfa.html')


@app.route('/apply')
@login_required
def apply():
    if not current_user.mfa_enabled:
        return redirect(url_for('setup_user_mfa'))
    return redirect(url_for('apply_form'))


@app.route('/application/form', methods=["GET", "POST"])
@login_required
@csrf.exempt
def apply_form():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin'))

    if request.method == "POST":
        f = request.form
        try:
            name = f.get("name")
            email = f.get("email")
            pan = f.get("pan")
            purpose = f.get("purpose")
            phone = f.get("phone")
            age = int(f.get("age"))
            income = int(f.get("income"))
            term = int(f.get("term"))
            amount = int(f.get("amount"))
        except Exception:
            return jsonify({"success": False, "message": "Invalid numeric values."}), 400

        errors = check_eligibility(age, income)
        if errors:
            return jsonify({"success": False, "message": errors[0]}), 400

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

        return jsonify({"success": True, "redirect_url": url_for("success", app_id=app_id)})

    return render_template("apply.html", verified_phone="MFA Verified")


@app.route('/success')
@login_required
def success():
    return render_template("success.html", app_id=request.args.get('app_id'))


@app.route('/status', methods=['GET', 'POST'])
def status():
    application_status = None
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        app_record = Application.query.get(app_id)
        if app_record:
            commitment_bytes = bytes.fromhex(app_record.commitment)
            signature_bytes = bytes.fromhex(app_record.signature)
            proof = {'t': app_record.proof_t, 's1': app_record.proof_s1, 's2': app_record.proof_s2}
            is_valid = verify_signature(public_key, commitment_bytes, signature_bytes) and \
                        verify_pedersen_opening(app_record.commitment, proof)

            application_status = {
                "name": app_record.name,
                "valid": is_valid,
                "status": app_record.status
            }

    return render_template("status.html", application=application_status, detail_view=False)


@app.route('/application/<uuid:app_id>')
@login_required
def application_status(app_id):
    app_record = Application.query.filter_by(id=str(app_id), user_id=current_user.id).first_or_404()
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
        'status': app_record.status
    }

    return render_template("status.html", application=data, is_zkp_valid=is_zkp_valid, detail_view=True)


@app.route('/application/<uuid:app_id>/withdraw', methods=['POST'])
@login_required
def withdraw_application(app_id):
    app_record = Application.query.filter_by(id=str(app_id), user_id=current_user.id).first()
    if not app_record:
        flash("Application not found.", "danger")
    elif app_record.status in ['APPROVED', 'REJECTED']:
        flash("Cannot withdraw finalized application.", "warning")
    else:
        db.session.delete(app_record)
        db.session.commit()
        flash("Application withdrawn.", "success")
    return redirect(url_for('dashboard'))


@app.route('/application/<uuid:app_id>/update', methods=['POST'])
@login_required
def update_application(app_id):
    app_record = Application.query.filter_by(id=str(app_id), user_id=current_user.id).first_or_404()
    if app_record.status != 'PENDING':
        flash("Cannot update finalized application.", "danger")
        return redirect(url_for('application_status', app_id=app_id))

    try:
        new_email = request.form.get('email') or decrypt_data(app_record.encrypted_email)
        new_pan = request.form.get('pan') or decrypt_data(app_record.encrypted_pan)
        new_age = int(request.form.get('age') or decrypt_data(app_record.encrypted_age))
        new_income = int(request.form.get('income') or decrypt_data(app_record.encrypted_income))
        new_purpose = request.form.get('purpose') or decrypt_data(app_record.encrypted_purpose)
        new_term = int(request.form.get('term') or decrypt_data(app_record.encrypted_term))

        errors = check_eligibility(new_age, new_income)
        if errors:
            flash(errors[0], 'danger')
            return redirect(url_for('application_status', app_id=app_id))

        app_record.encrypted_email = encrypt_data(new_email)
        app_record.encrypted_pan = encrypt_data(new_pan.upper())
        app_record.encrypted_age = encrypt_data(str(new_age))
        app_record.encrypted_income = encrypt_data(str(new_income))
        app_record.encrypted_purpose = encrypt_data(new_purpose)
        app_record.encrypted_term = encrypt_data(str(new_term))
        db.session.commit()
        flash("Application updated.", "success")
    except Exception as e:
        flash("Error updating: " + str(e), "danger")

    return redirect(url_for('application_status', app_id=app_id))


@app.route('/application/<uuid:app_id>/get_token')
@login_required
def get_blind_token(app_id):
    app_record = Application.query.filter_by(id=str(app_id), user_id=current_user.id).first_or_404()
    if app_record.status != 'APPROVED':
        flash("Token available only after approval.", "warning")
        return redirect(url_for('application_status', app_id=app_id))

    try:
        signed_blinded_int = int(app_record.blind_signature)
        r = int(app_record.blinding_factor_r)
        N = int(current_user.blind_N)
        final_sig = unblind_signature(signed_blinded_int, r, N)
        return render_template("token_display.html", token=final_sig, app_id=str(app_id))
    except Exception as e:
        flash("Unblinding failed: " + str(e), "danger")
        return redirect(url_for('application_status', app_id=app_id))


@app.route('/application/<uuid:app_id>/certificate')
@login_required
def application_certificate(app_id):
    # Only the owner of the application can view/download the certificate
    app_record = Application.query.filter_by(id=str(app_id), user_id=current_user.id).first_or_404()

    if app_record.status != 'APPROVED':
        flash("Certificate is available only for approved applications.", "warning")
        return redirect(url_for('application_status', app_id=app_id))

    try:
        signed_blinded_int = int(app_record.blind_signature)
        r = int(app_record.blinding_factor_r)
        N_user = int(current_user.blind_N)

        # Unblind to get the final token (blind signature)
        token_hex = unblind_signature(signed_blinded_int, r, N_user)

        # Minimal privacy-preserving data
        commitment_hex = app_record.commitment
        pub_N = str(BLIND_PUB_N)
        pub_e = str(BLIND_PUB_E)

        qr_payload = {
            "app_id": app_record.id,
            "commitment": commitment_hex,
            "token": token_hex,
            "N": pub_N,
            "e": pub_e,
        }
        qr_json = json.dumps(qr_payload, separators=(",", ":"))

        img = qrcode.make(qr_json)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

        issued_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        return render_template(
            "certificate.html",
            app_id=app_record.id,
            commitment=commitment_hex,
            token=token_hex,
            N=pub_N,
            e=pub_e,
            issued_at=issued_at,
            qr_code_image=qr_code_b64,
        )

    except Exception as e:
        flash("Could not generate certificate: " + str(e), "danger")
        return redirect(url_for('application_status', app_id=app_id))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If a USER is logged in → force logout user
    if current_user.is_authenticated and isinstance(current_user, User):
        logout_user()
        session.clear()

    # If admin is already logged in → go to admin dashboard
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and bcrypt.check_password_hash(admin.password_hash, password):
            login_user(admin)
            session['user_type'] = 'Admin'
            return redirect(url_for('admin'))

        flash("Invalid admin credentials.", "danger")

    return render_template("admin_login.html")


@app.route('/admin')
@login_required
def admin():
    if not isinstance(current_user, Admin):
        return redirect(url_for('admin_login'))

    admin_user = current_user
    apps = Application.query.all()
    apps_data = []
    processed_any = False

    for app_record in apps:
        commitment_bytes = bytes.fromhex(app_record.commitment)
        signature_bytes = bytes.fromhex(app_record.signature)
        proof = {'t': app_record.proof_t, 's1': app_record.proof_s1, 's2': app_record.proof_s2}

        is_valid = verify_signature(public_key, commitment_bytes, signature_bytes) and \
                   verify_pedersen_opening(app_record.commitment, proof)

        prediction = app_record.status.replace("_", " ")
        explanations = []

        if app_record.status == 'PENDING':
            processed_any = True

            if is_valid and loan_approval_model is not None:
                try:
                    age = int(decrypt_data(app_record.encrypted_age))
                    income = int(decrypt_data(app_record.encrypted_income))
                    term = int(decrypt_data(app_record.encrypted_term))
                    amount = app_record.amount

                    df = pd.DataFrame({
                        'Age': [age],
                        'Income': [income],
                        'Credit_Score': [750],  # fixed placeholder score
                        'Loan_Amount': [amount],
                        'Loan_Term': [term],
                        'Employment_Status_Unemployed': [0]
                    })

                    cols = [
                        'Age', 'Income', 'Credit_Score',
                        'Loan_Amount', 'Loan_Term',
                        'Employment_Status_Unemployed'
                    ]

                    features = df[cols]

                    if scaler is not None:
                        features_scaled = scaler.transform(features)
                    else:
                        features_scaled = features

                    result = loan_approval_model.predict(features_scaled)[0]

                    if result == 1:
                        app_record.status = 'APPROVED'
                        prediction = "Approved"

                        blinded_int = int(app_record.blind_signature)
                        signed_blinded = sign_blinded_message(
                            blinded_int,
                            int(admin_user.blind_priv_N),
                            int(admin_user.blind_priv_d)
                        )
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

    if processed_any:
        flash("Processing Complete: Applications reviewed.", "processing-successful")

    return render_template("admin.html", applications=apps_data)


if __name__ == "__main__":
    app.run()

