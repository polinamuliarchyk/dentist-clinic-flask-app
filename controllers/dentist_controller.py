from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload

from database import Session
from users.review import Review
from users.dentist import Dentist

dentist_bp = Blueprint("dentist", __name__)


@dentist_bp.route('/dentists_list')
def show_dentists():
    """
    Displays a list of dentists and their assigned clients (if any).

    Returns:
        str: The rendered content of the 'dentists_list.html' template, containing a list of dentists and their associated clients.
    """
    db = Session()
    try:
        dentists = db.query(Dentist).options(
            joinedload(Dentist.client_associations).joinedload(Review.client)
        ).all()
        return render_template('dentists_list.html', dentists=dentists)
    finally:
        db.close()