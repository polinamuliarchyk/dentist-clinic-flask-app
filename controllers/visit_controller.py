from datetime import datetime, timedelta, date
from random import choice

from django.contrib.auth.decorators import login_required
from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from sqlalchemy.orm import joinedload, contains_eager

from models.service import Service
from models.visit import Visit
from database import Session
from users.client import Client
from users.person import Person
from users.dentist import Dentist

visit_bp = Blueprint("visit", __name__)

@login_required
@visit_bp.route("/book-visit", methods=["GET", "POST"])
def choose_visit():
    """
    Enables customers to select services before booking an appointment.

    GET:
        Retrieves a list of available services from the database and renders a service selection form.

    POST:
        Saves the selected services to the session and redirects the user to the appointment selection page.

    Returns:
         str | Response: Rendered page with the form or a redirect to the appointment selection page.
    """
    if request.method == 'POST':
        service_ids = request.form.getlist('service_ids')

        if not service_ids:
            flash("Please select at least one service.")
            return redirect(url_for('visit.choose_visit'))

        session['chosen_services'] = service_ids

        return redirect(url_for('visit.select_date_slot'))

    db = Session()
    services = db.query(Service).all()
    db.close()
    return render_template('choose_services.html', services=services)


def generate_dates(days=30):
    """
    Generates available appointment slots for the coming working days.

    Returns:
        list[str]: A list of available dates on working days.
    """
    dates = []
    today = datetime.today()
    for i in range(days):
        day = today + timedelta(days=i)
        if day.weekday() < 5:
            dates.append(day.strftime("%Y-%m-%d"))
    return dates


@visit_bp.route("/select-date-slot", methods=["GET", "POST"])
def select_date_slot():
    """
    Handles the selection of a date and dentist for a planned appointment.

    GET:
        Renders a form with a list of available dates and dentists.

    POST:
        Saves the selected date and dentist to the session, then redirects
        to the client details form.

    Returns:
        str | Response: Rendered appointment selection page or redirect.
    """
    db = Session()
    try:
        if request.method == "POST":
            selected_date = request.form.get("visit_date")
            dentist_id = request.form.get("dentist_id")

            print(f"DEBUG: Received date={selected_date}, dentist={dentist_id}")

            if selected_date and dentist_id:
                session["visit_date"] = selected_date
                session["dentist_id"] = dentist_id
                return redirect(url_for("visit.verify_data"))

            flash("Please select both a date and a dentist.")

        available_dates = generate_dates(30)
        dentists = db.query(Person).filter_by(type='dentist').all()

        return render_template("choose_time_slot.html", dates=available_dates, dentists=dentists)
    finally:
        db.close()


@visit_bp.route("/verify-data", methods=["GET", "POST"])
def verify_data():
    """
    Handles the final stage of booking an appointment – data confirmation.

    GET:
        Retrieves client, dentist, service data, and the selected date from the session.
        Displays an appointment summary and a form to confirm or cancel.

    POST:
        Based on the selected action ('confirm' or 'cancel'):
        - Creates and saves the appointment in the database if the slot is available.
        - Sets the appropriate status.
        - Handles database save exceptions.

    Returns:
        str | Response: Rendered confirmation page or redirect.
    """
    db = Session()
    try:
        visit_date_str = session.get("visit_date")
        dentist_id = session.get("dentist_id")
        client_id = session.get("client_id")
        chosen_services_ids = session.get("chosen_services", [])

        print(f"DEBUG: date={visit_date_str}, dentist={dentist_id}, client={client_id}, services={chosen_services_ids}")

        if not all([visit_date_str, dentist_id, client_id]) or not chosen_services_ids:
            flash("Some data is missing. Please select date and dentist again.")
            return redirect(url_for("visit.select_date_slot"))

        if request.method == "POST":
            action = request.form.get("action")
            data_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()

            if action == "confirm":
                exists = db.query(Visit).filter_by(visit_date=data_date, dentist_id=dentist_id).first()
                if exists:
                    flash("This time slot is already taken.")
                    return redirect(url_for("visit.select_date_slot"))

                assistants = db.query(Person).filter_by(type='assistant').all()
                assistant_id = choice(assistants).id if assistants else None

                visit = Visit(
                    visit_date=data_date,
                    dentist_id=dentist_id,
                    client_id=client_id,
                    assistant_id=assistant_id,
                    status="Scheduled"
                )

                services = db.query(Service).filter(Service.id.in_(chosen_services_ids)).all()
                visit.services.extend(services)

                try:
                    db.add(visit)
                    db.commit()
                    flash("The appointment has been confirmed.")

                    session.pop("visit_date", None)
                    session.pop("chosen_services", None)
                    session.pop("dentist_id", None)

                    return redirect(url_for("client.index"))
                except Exception as e:
                    db.rollback()
                    flash(f"Error: {e}")

            elif action == "cancel":
                session.pop("visit_date", None)
                session.pop("chosen_services", None)
                return redirect(url_for("client.index"))

        client = db.query(Client).get(client_id)
        dentist = db.query(Dentist).get(dentist_id)
        services = db.query(Service).filter(Service.id.in_(chosen_services_ids)).all()
        total_price = sum(s.price for s in services)

        return render_template(
            "confirmation.html",
            visit_date=visit_date_str,
            dentist=dentist,
            client=client,
            services=services,
            total_price=total_price
        )
    finally:
        db.close()


@visit_bp.route("/visit-history")
def visit_history():
    """
    Displays the logged-in client's appointment history with filtering and sorting options.
    """
    client_id = session.get("client_id")

    if not client_id:
        flash("Please log in to view your history.")
        return redirect(url_for("auth.login"))

    search_query = request.args.get("search", "").strip()
    date_str = request.args.get("date")
    sorting = request.args.get("sorting", "desc")

    db = Session()
    try:
        query = (
            db.query(Visit)
            .join(Visit.dentist)
            .options(
                contains_eager(Visit.dentist),
                joinedload(Visit.services)
            )
            .filter(Visit.client_id == client_id)
        )

        if search_query:
            query = query.filter(Dentist.lastname.ilike(f"%{search_query}%"))

        if date_str:
            try:
                data_filter = datetime.strptime(date_str, "%Y-%m-%d").date()
                query = query.filter(Visit.visit_date == data_filter)
            except ValueError:
                pass

        if sorting == "asc":
            query = query.order_by(Visit.visit_date.asc())
        else:
            query = query.order_by(Visit.visit_date.desc())

        visits = query.all()

        print(f"DEBUG: Found {len(visits)} visits for client {client_id}")

        for visit in visits:
            visit.total_price = sum(service.price for service in visit.services)

        return render_template("visit_history.html",
                               visits=visits,
                               today=date.today())
    finally:
        db.close()




@visit_bp.route("/cancel-visit/<int:visit_id>", methods=["POST"])
def cancel_visit(visit_id):
    """
    Cancels an upcoming client appointment.
    """
    client_id = session.get("client_id")
    if not client_id:
        flash("Access denied. Please provide your details first.")
        return redirect(url_for("client.enter_details"))

    db = Session()
    try:
        visit = db.query(Visit).filter_by(id=visit_id, client_id=client_id).first()

        if not visit:
            flash("Appointment not found.")
            return redirect(url_for("visit.visit_history"))

        if visit.visit_date <= date.today():
            flash("You cannot cancel past appointments.")
            return redirect(url_for("visit.visit_history"))

        visit.status = "Cancelled"
        try:
            db.commit()
            flash("The appointment has been cancelled.")
        except Exception as e:
            db.rollback()
            flash(f"Error cancelling appointment: {e}")

        return redirect(url_for("visit.visit_history"))
    finally:
        db.close()


@visit_bp.route("/delete-visit/<int:visit_id>", methods=["POST"])
def delete_visit(visit_id):
    """
    Removes an appointment from the database if it is completed or canceled.
    """
    client_id = session.get("client_id")
    if not client_id:
        flash("Access denied. Please provide your details first.")
        return redirect(url_for("client.enter_details"))

    db = Session()
    try:
        visit = db.query(Visit).filter_by(id=visit_id, client_id=client_id).first()
        if not visit:
            flash("No appointment found to delete.")
            return redirect(url_for("visit.visit_history"))

        if visit.status not in ["Cancelled", "Completed"]:
            flash("You can only delete appointments with a 'Cancelled' or 'Completed' status.")
            return redirect(url_for("visit.visit_history"))

        try:
            db.delete(visit)
            db.commit()
            flash("The appointment has been deleted.")
        except Exception as e:
            db.rollback()
            flash(f"Error deleting appointment: {e}")

        return redirect(url_for("visit.visit_history"))
    finally:
        db.close()