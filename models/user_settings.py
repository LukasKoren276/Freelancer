from sqlalchemy import Column, Integer, String
from . import Base


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_first_name = Column(String(50), nullable=True)
    user_last_name = Column(String(50), nullable=True)
    user_company_registration_number = Column(String(50), nullable=True)
    user_street = Column(String(100), nullable=True)
    user_street_number = Column(Integer, nullable=True)
    user_city = Column(String(50), nullable=True)
    user_country = Column(String(50), nullable=True)
    user_registered_as = Column(String(255), nullable=True)
    invoice_due_date = Column(Integer, nullable=False)
    rate_per_hour = Column(Integer, nullable=False)
    currency = Column(String(10), nullable=True)
    vat = Column(Integer, nullable=True)

    def __repr__(self):
        return (f"<UserSettings(user_first_name={self.user_first_name}, "
                f"user_last_name={self.user_last_name}, "
                f"user_company_registration_number={self.user_company_registration_number}, "
                f"user_street={self.user_street}, "
                f"user_street_number={self.user_street_number}, "
                f"user_city={self.user_city}, "
                f"user_country={self.user_country}, "
                f"user_registered_as={self.user_registered_as}, "
                f"invoice_due_date={self.invoice_due_date}, "
                f"currency={self.currency}, vat={self.vat})>")
