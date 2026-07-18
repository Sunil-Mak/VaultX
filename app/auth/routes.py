from flask import render_template, request, redirect, url_for, flash

from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # Login logic will be added next
        return redirect(url_for("dashboard.index"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Save the user
        pass

    return render_template("register.html")
