from flask import Blueprint, session, flash, redirect, url_for, render_template, request
from ..services.admin_service import admin_required
from ...config import Config

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Config.ADMIN_USERNAME == username and Config.ADMIN_PASSWORD == password:
            session["admin_logged_in"] = True
            flash("Login successful!", "success")
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("admin_login.html")

    return render_template("admin_login.html")


@admin_bp.route("/dashboard", methods=["GET", "POST"])
@admin_required
def admin_dashboard():
    return render_template("admin_dashboard.html")


