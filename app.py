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
    # In a real app, use Flask-Login
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Import and register routes/blueprints
    from routes import main 
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    # When running directly, use the factory to create the app instance
    app = create_app()
    app.run(debug=True)

# Note: The recommended way to run is "flask run --debug" after setting FLASK_APP=app