from datetime import date
from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, attribute_mapped_collection

from users.employee import Employee


class Receptionist(Employee):
    __tablename__ = 'receptionist'
    work_phone = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'receptionist'
    }

    workschedule = relationship(
        "WorkSchedule",
        collection_class=attribute_mapped_collection("date"),
        back_populates="receptionist"
    )

    def calculate_salary_increase(self) -> float:
        """
        Calculates the salary increase for the Receptionist based on their current salary.

        The pay rise is 5% of the employee’s current salary.

        Returns:
            float: The amount of the salary increased.
        """
        salary_increase = self._salary * 0.05
        return salary_increase

    def view_schedule(self, day: date) -> Optional["WorkSchedule"]:
        """
        Returns the receptionist's work schedule for a specific day.

        Args:
            day (date): The day for which the schedule is to be returned.

        Returns:
            work_schedule | None: A work schedule object for the specified day, or None if no entry is found.
        """
        return self.workschedule.get(day)
