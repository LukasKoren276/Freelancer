from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .customer import Customer
from .project import Project
from .item import Item
from .item_time import ItemTime
from .invoice import Invoice
from .user_settings import UserSettings
