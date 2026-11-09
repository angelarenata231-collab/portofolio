import os

from flask import Flask
from flask_login import LoginManager

from config import config
from models import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[env])

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models import seed_data

        db.create_all()
        seed_data()

    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.contact import contact_bp
    from routes.portfolio import portfolio_bp
    from routes.upload import upload_bp

    app.register_blueprint(portfolio_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(upload_bp, url_prefix="/upload")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
