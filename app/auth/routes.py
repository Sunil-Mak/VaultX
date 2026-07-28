from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_bp
from ..extensions import db
from ..models import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("No account found with this email.", "danger")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)

        user.last_login = datetime.utcnow()
        db.session.commit()

        flash(f"Welcome back, {user.name}!", "success")

        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password:
            flash("Fill all fields.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            created_at=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("dashboard.index"))