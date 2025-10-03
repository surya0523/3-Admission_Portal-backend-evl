from app import db # Correct import from the uninitialized db object
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    program = db.Column(db.String(50), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Status: 'Pending', 'Approved', 'Rejected'
    status = db.Column(db.String(10), nullable=False, default='Pending') 
    
    # Unique token for status check/notification
    status_token = db.Column(db.String(32), unique=True, nullable=False) 

    def __repr__(self):
        return f"Applicant('{self.full_name}', '{self.email}', '{self.status}')"

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)