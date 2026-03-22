from datetime import date

from sqlalchemy import Column, String, ForeignKey, Integer, Date, event
from sqlalchemy.orm import relationship, composite
from werkzeug.security import generate_password_hash, check_password_hash

from users.person import Person, Base


class Address:
    def __init__(self, street, city, zipcode):
        self.street = street
        self.city = city
        self.zipcode = zipcode

    def __composite_values__(self):
        return self.street, self.city, self.zipcode


class Client(Person):
    __tablename__ = "client"
    __mapper_args__ = {
        "polymorphic_identity": "client"
    }

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    phone = Column(String)
    date_of_birth = Column(Date)
    second_name = Column(String, nullable=True)
    discount_code = Column(Integer, nullable=True)
    age = Column(Integer)
    street = Column(String)
    city = Column(String)
    zipcode = Column(String)
    password_hash = Column(String)

    allergies = relationship("Allergy", back_populates="client", cascade="all, delete-orphan")
    dentist_associations = relationship("Review", back_populates="client")
    address = composite(Address, street, city, zipcode)

    visits = relationship("Visit", back_populates="client")
    recommendations = relationship("Recommendation", back_populates="client", cascade="all, delete-orphan", collection_class=list)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def calculate_age(birthdate: date) -> int:
    """
    Calculates age based on the date of birth.

    Age is calculated as the number of full years, taking into account the day and month of birth
    relative to the current date.

    Args:
        birthdate (date): The person’s date of birth.

    Returns:
        int: The calculated age in years.
    """
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )


@event.listens_for(Client, 'before_insert')
def set_age_before_insert(mapper, connection, target):
    """
       Sets the `age` field of the `Client` object before it is added to the database.

       If the `Client` object has a date of birth (`date_of_birth`) set,
       the function will calculate the age and assign it to the `age` field.

       Args:
           target: The `Client` object to be saved.
       """
    if target.date_of_birth:
        target.age = calculate_age(target.date_of_birth)


@event.listens_for(Client, 'before_update')
def set_age_before_update(mapper, connection, target):
    """
      Updates the `age` field of the `Client` object before it is updated in the database.

      If the `date_of_birth` field is set, the function calculates the new age
      and assigns it to the `age` field.

      Args:
          target: The `Client` object to be updated.
      """
    if target.date_of_birth:
        target.age = calculate_age(target.date_of_birth)


class Allergy(Base):
    __tablename__ = 'allergy'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)

    client = relationship("Client", back_populates="allergies")



