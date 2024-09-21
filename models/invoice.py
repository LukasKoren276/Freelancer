from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base


class Invoice(Base):
    __tablename__ = 'invoices'

    invoice_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'), nullable=False)
    issued_at = Column(DateTime, nullable=False)
    note = Column(String(255), nullable=True)

    project = relationship('Project', back_populates='invoices')

    __table_args__ = (
        UniqueConstraint('project_id', name='uix_invoice_project_id'),
    )

    def __repr__(self):
        return (f"<Invoice(id={self.invoice_id}, project_id={self.project_id}, "
                f"issued_at={self.issued_at}, note={self.note})>")
