from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user

from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@auth_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            login_user(user)

            return redirect(
                url_for("dashboard.dashboard")
            )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect("/")