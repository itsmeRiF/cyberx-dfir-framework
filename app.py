from flask import Flask, redirect, url_for
from config import Config
from database.db import db

from routes.auth import auth_bp, login_manager
from routes.dashboard import dashboard_bp
from routes.cases import cases_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cases_bp)
    with app.app_context():
        db.create_all()

    # IMPORTANT: root route MUST redirect
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=1337)