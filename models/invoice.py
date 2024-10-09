from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from . import Base


class Invoice(Base):
    __tablename__ = 'invoices'

    invoice_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    issued_at = Column(DateTime, nullable=False)
    note = Column(String(255), nullable=True)

    item = relationship('Item', back_populates='invoices')

    def __repr__(self):
        return (f"<Invoice(id={self.invoice_id}, item_id={self.item_id}, "
                f"issued_at={self.issued_at}, note={self.note})>")
