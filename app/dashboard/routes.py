from flask import render_template

from . import dashboard_bp


@dashboard_bp.route("/")
def index():
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
