from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from users.employee import Employee


class Assistant(Employee):
    __tablename__ = 'assistant'
    specialization = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'assistant'
    }

    visits = relationship("Visit", back_populates="assistant")
    labtests = relationship("Labtest", back_populates="assistant")

    def calculate_salary_increase(self) -> float:
        """
        Calculates the amount of the salary increase for the Assistant based on their current salary.

        The salary increase is 10% of the employee’s current salary.

        Returns:
            float: The amount of the salary increase.
        """
        salary_increase = self._salary/10
        return salary_increase