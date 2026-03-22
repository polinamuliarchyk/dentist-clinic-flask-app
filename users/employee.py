import abc
from abc import ABC

from sqlalchemy import Column, Integer, ForeignKey, Float, Date, CheckConstraint, Enum as SqlEnum

from users.Enum import ContractEnum
from users.person import Person


class Employee(Person):
    __abstract__ = True
    __mapper_args__ = {
        "polymorphic_identity": "employee"
    }

    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    date_of_employment = Column(Date)
    employee_number = Column(Integer, unique=True)
    _salary = Column("salary", Float)
    contract = Column(SqlEnum(ContractEnum, name="contract_enum", native_enum=False), nullable=False)

    __table_args__ = (
        CheckConstraint("salary >= 4000 AND salary <= 20000"),
    )

    @abc.abstractmethod
    def calculate_salary_increase(self) -> float:
        """
           An abstract method for calculating an employee’s salary increase.

           It should be implemented in the subclasses (Dentist, Assistant, Receptionist)
           according to their respective salary increase.

           Returns:
               float: The amount of the salary increase.
           """
        pass

    @staticmethod
    def promote_assistant_to_dentist(session, assistant_id, experience: int):
        """
          Replaces the Assistant object with a Dentist object, retaining shared data
          and assigned roles. This operation simulates a "promotion" within the system.

          Process:
          - Retrieves the Assistant based on `assistant_id`.
          - Saves their data.
          - Deletes the Assistant object from the database.
          - Creates a new Dentist object with the retained data and a new `experience` field.
          - Adds the new Dentist to the database and commits the changes.

          Args:
              session (Session): SQLAlchemy session for communicating with the database.
              assistant_id (int): The ID of the assistant to be promoted.
              experience (int): The experience value assigned to the new dentist.
          """
        from users.assistant import Assistant
        assistant = session.query(Assistant).get(assistant_id)
        if not assistant:
            raise ValueError("The assistant does not exist.")

        name = assistant.name
        lastname = assistant.lastname
        date_of_employment = assistant.date_of_employment
        employee_number = assistant.employee_number
        roles = list(assistant.roles)

        session.delete(assistant)
        session.flush()

        from users.dentist import Dentist
        new_dentist = Dentist(
            name=name,
            lastname=lastname,
            date_of_employment=date_of_employment,
            employee_number=employee_number,
            experience=experience
        )
        new_dentist.roles = roles

        session.add(new_dentist)
        session.commit()

