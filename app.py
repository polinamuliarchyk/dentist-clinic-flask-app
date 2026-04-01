from flask import Flask

from controllers.auth_controller import auth_bp
from controllers.client_controller import client_bp
from controllers.dentist_controller import dentist_bp
from controllers.service_controller import service_bp
from controllers.visit_controller import visit_bp
from database import engine, Base

from models.notification import Notification
from models.recommendation import Recommendation

from models.labtest import Labtest
from users.person import Base, Person
from models.visit import Visit
from users.dentist import Dentist
from users.client import Client, Allergy, Address
from users.assistant import Assistant
from models.service import Service

from models.work_schedule import WorkSchedule
from users.review import Review
from users.Enum import ContractEnum
from users.receptionist import Receptionist

app = Flask(__name__)

def create_app():
    app.secret_key = "your_secret_key"

    app.register_blueprint(client_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(dentist_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(auth_bp)

    return app


from datetime import date
from werkzeug.security import generate_password_hash
from database import Session
from users.client import Client


def seed_database():
    db = Session()

    if db.query(Service).count() > 0:
        print("База данных уже заполнена. Если хочешь пересоздать данные, удали файл базы.")
        db.close()
        return


    services = [
        Service(name="Dental Consultation", price=150.00, description="Comprehensive dental checkup and consultation."),
        Service(name="Teeth Whitening", price=800.00, description="Professional laser teeth whitening."),
        Service(name="Cavity Filling", price=250.00, description="Composite resin filling for a single cavity."),
        Service(name="Root Canal", price=1200.00,
                description="Endodontic therapy to treat infection at the centre of a tooth."),
        Service(name="Tooth Extraction", price=300.00, description="Safe removal of a damaged or problematic tooth.")
    ]
    db.add_all(services)

    dentists = [
        Dentist(name="Gregory", lastname="House", experience=15, type="dentist", contract="B2B"),
        Dentist(name="Sarah", lastname="Connor", experience=8, type="dentist", contract="FULLTIME"),
        Dentist(name="Alan", lastname="Grant", experience=20, type="dentist", contract="PARTTIME")
    ]
    db.add_all(dentists)

    assistants = [
        Person(name="Clara", lastname="Oswald", type="assistant"),
        Person(name="Rory", lastname="Williams", type="assistant")
    ]
    db.add_all(assistants)

    test_password = generate_password_hash("1234")

    clients = [
        Client(name="John", lastname="Smith", phone="111222333", date_of_birth=date(1985, 4, 12), street="Maple St 12",
               city="New York", zipcode="10001", password_hash=test_password),
        Client(name="Emma", lastname="Johnson", phone="444555666", date_of_birth=date(1992, 8, 25), street="Oak Ave 45",
               city="Boston", zipcode="02108", password_hash=test_password),
        Client(name="Michael", lastname="Ivanov", phone="999888777", date_of_birth=date(1890, 1, 1),
               street="Tverskaya 1", city="Moscow", zipcode="101000", password_hash=test_password)
    ]
    db.add_all(clients)

    try:
        db.commit()
        print("Успех! Сгенерированы:")
        print(f"— {len(services)} услуг")
        print(f"— {len(dentists)} стоматологов")
        print(f"— {len(assistants)} ассистентов")
        print(f"— {len(clients)} клиентов (Пароль для входа: 1234)")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении в базу: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed_database()
    app = create_app()
    app.run(debug=True)