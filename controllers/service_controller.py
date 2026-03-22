from flask import render_template, Blueprint

from models.service import Service
from database import Session

service_bp = Blueprint("service", __name__)


@service_bp.route('/service')
def show_services():
    """
    Displays all available dental services.

    Returns:
        str: The rendered content of the 'services_list.html' template with the provided list of services.
    """
    db = Session()
    try:
        services = db.query(Service).all()
        return render_template('services_list.html', services=services)
    finally:
        db.close()