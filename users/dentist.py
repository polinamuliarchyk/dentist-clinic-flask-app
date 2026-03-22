from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, func
from sqlalchemy.orm import relationship

from users.employee import Employee


class Dentist(Employee):
    __tablename__ = 'dentist'
    experience = Column(Integer)
    max_number_of_visits_per_day = Column(Integer, default=5)

    __mapper_args__ = {
        'polymorphic_identity': 'dentist',
    }

    client_associations = relationship("Review", back_populates="dentist")
    visits = relationship("Visit", back_populates="dentist")
    labtests = relationship("Labtest", back_populates="dentist", order_by="Visit.visit_date")

    def calculate_salary_increase(self) -> float:
        """
        Calculates the salary increase for a dentist based on their current salary.

        The pay rise is 1,500 PLN for each year of experience.

        Returns:
            float: The amount of the salary increase.
        """
        salary_increase = self.experience * 1500
        return salary_increase

    @classmethod
    def the_most_active_dentists(cls, session, days=30, limit=5):
        """
        Returns a list of the most active dentists within a specified period.

        Activity is measured by the number of appointments carried out by the dentist in the last `days`.

        Args:
            session (Session): An SQLAlchemy session object.
            days (int): The number of days back from which visits are to be included (default 30).
            limit (int): The maximum number of dentists to return (default 5).

        Returns:
            list[tuple(Dentist, int)]: A list of tuples containing `Dentist` objects and the number of visits,
            sorted in descending order by the number of visits.
       """

        date_from = datetime.now() - timedelta(days=days)

        from models.visit import Visit
        return (
            session.query(cls, func.count(Visit.id).label("count_of_visits"))
            .join(Visit, Visit.dentist_id == cls.id)
            .filter(Visit.visit_date >= date_from)
            .group_by(cls.id)
            .order_by(func.count(Visit.id).desc())
            .limit(limit)
            .all()
        )