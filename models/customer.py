from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    street = Column(String(100), nullable=False)
    street_number = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    company_registration_number = Column(String(50), nullable=False)

    projects = relationship('Project', order_by='Project.project_id', back_populates='customer')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    __table_args__ = (
        UniqueConstraint(
            'first_name',
            'last_name',
            'street',
            'street_number',
            'city',
            name='uix_customer_unique'
        ),
    )
