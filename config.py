import os

class Config:
    # A secure key is mandatory for Flask-WTF forms and session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed_in_prod'
    
    # Database Configuration (Using SQLite for simplicity)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration (Replace with your actual mail server details)
    # NOTE: You MUST set EMAIL_USER and EMAIL_PASS environment variables
    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER') or 'your_default_email@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') or 'your_app_password'
    ADMIN_EMAIL = 'admin@yourcollege.edu' 
    
    # Placeholder for SMS API details (e.g., Twilio credentials)
    # SMS functions will print to console unless Twilio is fully configured
    SMS_ACCOUNT_SID = 'ACxxxxxxxxxxxxxxxxxxxxxxx'
    SMS_AUTH_TOKEN = 'your_auth_token_here'
    SMS_FROM_NUMBER = '+1501712266'