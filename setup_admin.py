from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_bcrypt import Bcrypt
from getpass import getpass
import random

# Import database and model classes
# NOTE: Ensure database.py is the latest version
from database import db, Admin
from blind_signature_utils import generate_blind_keys 

# --- CONFIGURATION (Must match app.py) ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///privyloans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24) 

db.init_app(app)
bcrypt = Bcrypt(app)

def create_admin():
    """Creates the initial admin user with necessary crypto keys."""
    with app.app_context():
        db.create_all() # Ensure tables exist

        username = 'admin'
        if Admin.query.filter_by(username=username).first():
            print(f"Admin user '{username}' already exists.")
            return

        print("--- Create PrivyLoans Admin User ---")
        password = getpass(f"Enter password for admin user '{username}': ")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Generate Blind Signature Keys for the Admin
        BLIND_KEYS = generate_blind_keys()
        
        # Create new Admin instance (MFA fields are now REMOVED)
        new_admin = Admin(
            username=username,
            password_hash=hashed_password,
            # Assign all Blind Signature keys to the Admin record
            blind_priv_N=str(BLIND_KEYS['N']),
            blind_priv_e=str(BLIND_KEYS['e']),
            blind_priv_d=str(BLIND_KEYS['d'])
        )
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully!")
        print("Blind Signature Keys generated and stored in Admin record.")

if __name__ == '__main__':
    create_admin()