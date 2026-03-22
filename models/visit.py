from datetime import date
from multipledispatch import dispatch

from sqlalchemy import Column, Integer, ForeignKey, Date, String, Table
from sqlalchemy.orm import relationship, Session

from models.service import Service
from users.client import Client
from users.person import Base

visit_services = Table(
    'visit_services',
    Base.metadata,
    Column('visit_id', Integer, ForeignKey('visit.id'), primary_key=True),
    Column('service_id', Integer, ForeignKey('service.id'), primary_key=True)
)

class Visit(Base):
    __tablename__ = 'visit'

    id = Column(Integer, primary_key=True)
    visit_date = Column(Date)
    status = Column(String, default="pending")

    dentist_id = Column(Integer, ForeignKey('dentist.id'))
    client_id = Column(Integer, ForeignKey('client.id'))
    assistant_id = Column(Integer, ForeignKey('assistant.id'))


    services = relationship(
        "Service",
        secondary=visit_services,
        backref="associated_visits"
    )
    dentist = relationship("Dentist", back_populates="visits")
    assistant = relationship("Assistant", back_populates="visits")
    client = relationship("Client", back_populates="visits")
    notifications = relationship("Notification", back_populates="visits")


    @staticmethod
    @dispatch(str, str, Session)
    def edit_visit(name: str, visit_date: str, session: Session):
        """
        Edits a customer’s appointment date based on their first name.

        The user selects from a list of existing appointments and then enters a new date.
        The new date is saved to the database.

        Args:
            name (str): The customer’s first name.
            visit_date (str): New appointment date.
            session (Session): SQLAlchemy session.
        """
        client = session.query(Client).filter(Client.name == name).first()

        if not client:
            print(f"We don't have a customer named '{name}'")
            return

        clients_visits = session.query(Visit).filter(Visit.client_id == client.id).all()

        if not clients_visits:
            print("No appointments found")
            return

        print("\nVisits:")
        for idx, visit in enumerate(clients_visits, 1):
            print(f"{idx}. Date: {visit.visit_date}, Services: {[s.name for s in visit.services]}")

        try:
            choice = int(input("\nSelect the appointment to edit (0 to cancel): "))
            if choice == 0:
                print("The operation has been cancelled.")
                return
            if 1 <= choice <= len(clients_visits):
                visit = clients_visits[choice - 1]
                visit.visit_date = date.fromisoformat(visit_date)
                session.commit()
                print(f"The appointment date has been changed to {visit_date}")
            else:
                print("An incorrect number has been entered")
        except ValueError:
            print("Please enter a valid number")

    @staticmethod
    @dispatch(str, str, list, Session)
    def edit_visit(name: str, visit_date: str, services_id: list, session: Session):
        """
        Edits the date and assigned services for a customer visit.

        The user selects one of the existing customer visits,
        and then the new date and list of services are saved to the database.

        Args:
            name (str): The customer’s name.
            visit_date (str): New visit date.
            services_id (list): List of service IDs.
            session (Session): SQLAlchemy session.
        """
        if not all(isinstance(x, int) for x in services_id):
            raise TypeError("All elements in the list must be integers")

        with session.no_autoflush:
            client = session.query(Client).filter(Client.name == name).first()

        if not client:
            print(f"We do not have a customer named '{name}'")
            return

        services = session.query(Service).filter(Service.id.in_(services_id)).all()
        if len(services) != len(services_id):
            print("Some services do not exist")
            return

        clients_visits = session.query(Visit).filter(Visit.client_id == client.id).all()

        print("\nVisit:")
        for idx, visit in enumerate(clients_visits, 1):
            print(f"{idx}. Date: {visit.visit_date}, Services: {[s.name for s in visit.services]}")

        try:
            choice = int(input("\nSelect the appointment to edit (0 to cancel): "))
            if choice == 0:
                print("The operation has been cancelled")
                return
            if 1 <= choice <= len(clients_visits):
                visit = clients_visits[choice - 1]
                visit.visit_date = date.fromisoformat(visit_date)
                visit.services = services
                session.commit()
                print(f"The appointment date and services have been updated")
            else:
                print("An incorrect number has been entered")
        except ValueError:
            print("Please enter a valid number")

    def update_status(self):
        """
        Updates the visit status to 'Completed' if its date has already passed.

        The status is automatically updated only if `date` is earlier than today's date.
        """
        if self.visit_date and self.visit_date < date.today():
            self.status = "Completed"