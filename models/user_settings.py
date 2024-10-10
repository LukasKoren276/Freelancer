from sqlalchemy import Column, Integer, String
from . import Base


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=True)
    user_company_registration_number = Column(String(50), nullable=False)
    user_first_name = Column(String(50), nullable=False)
    user_last_name = Column(String(50), nullable=False)
    user_street = Column(String(100), nullable=False)
    user_street_number = Column(Integer, nullable=False)
    user_city = Column(String(50), nullable=False)
    user_country = Column(String(50), nullable=False)
    user_registered_as = Column(String(255), nullable=False)
    account_number = Column(String(20), nullable=False)
    bank_code = Column(String(20), nullable=False)
    invoice_due_date = Column(Integer, nullable=False)
    rate_per_hour = Column(Integer, nullable=False)
    currency = Column(String(10), nullable=False)
    vat = Column(Integer, nullable=True)

    def __repr__(self):
        return (f'<UserSettings(user_first_name={self.user_first_name}, '
                f'user_last_name={self.user_last_name}, '
                f'user_company_registration_number={self.user_company_registration_number}, '
                f'user_street={self.user_street}, '
                f'user_street_number={self.user_street_number}, '
                f'user_city={self.user_city}, '
                f'user_country={self.user_country}, '
                f'user_registered_as={self.user_registered_as}, '
                f'account_number={self.account_number} ',
                f'bank_code={self.bank_code} ',
                f'invoice_due_date={self.invoice_due_date}, '
                f'currency={self.currency}, vat={self.vat})>')
