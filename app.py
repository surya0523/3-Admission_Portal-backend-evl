from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    
    # Simple session setup (Required for the simple admin_required decorator)
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Import and register routes/blueprints
    from routes import main 
    app.register_blueprint(main)

    return app

# =========================================================================
# 🌟 Local Development Block (Used only when running 'python app.py')
# =========================================================================
if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run(debug=True)

# =========================================================================
# 🌟 Deployment/Gunicorn Block (Used when running 'gunicorn app:app')
# =========================================================================
# Gunicorn/Render will look for this global 'app' variable.
app = create_app()