from datetime import datetime

from flask import render_template, request, redirect, url_for, session, flash

from database import Session
from users.client import Client
from flask import Blueprint

client_bp = Blueprint("client", __name__)


@client_bp.route("/")
def index():
    """
    The application's home page.

    Returns:
        str: The rendered content of the 'index.html' template.
    """
    return render_template("index.html")


@client_bp.route("/registration", methods=["GET"])
def client_registration():
    """
      Renders the customer registration form.

      Returns:
          str: The rendered content of the 'client_registration.html' template.
      """
    return render_template("client_registration.html")

@client_bp.route("/register-client", methods=["POST"])
def register_client():
    """
       Registers a new customer based on the data submitted via the form.

       POST:
           - Creates a new Customer object.
           - Saves it to the database.
           - Saves the customer ID in the session.
           - Redirects to the data confirmation page.

       Returns:
           Response: Redirect to the data confirmation page.
       """
    data = request.form
    date_of_birth_str = data.get("date_of_birth")
    date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date() if date_of_birth_str else None

    client = Client(
        name=data.get("name"),
        lastname=data.get("lastname"),
        phone=data.get("phone"),
        date_of_birth=date_of_birth,
        street=data.get("street"),
        city=data.get("city"),
        zipcode=data.get("zipcode")
    )

    password = data.get("password")
    client.set_password(password)

    db = Session()
    try:
        db.add(client)
        db.commit()
        session["client_id"] = client.id
    except Exception as e:
        db.rollback()
        flash("Registration error. Phone number might already be in use.")
        return redirect(url_for("client.client_registration"))
    finally:
        db.close()

    return redirect(url_for("client.index"))



