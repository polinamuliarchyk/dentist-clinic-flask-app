from flask import Blueprint, request, redirect, url_for, render_template, flash, session


from database import Session
from users.client import Client
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles client login using phone number and password.
    """
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        db = Session()
        try:
            client = db.query(Client).filter_by(phone=phone).first()

            if client and client.check_password(password):
                session["client_id"] = client.id
                flash("Logged in successfully!")

                if session.get("dates") and session.get("chosen_services"):
                    return redirect(url_for("visit.verify_data"))
                return redirect(url_for("client.index"))
            else:
                flash("Invalid phone number or password.")
        finally:
            db.close()

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Logs the user out."""
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("client.index"))