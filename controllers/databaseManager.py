from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from helpers.constants import Constants as Const
from models import Customer, UserSettings, Base, Project, Item


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def get_entities(self, entity_type: Base) -> Base | None:
        return self.session.query(entity_type).all()

    def get_active_entities(self, entity: Base):
        return self.session.query(entity).filter(entity.status == Const.status_active).all()

    def save_entity(self, entity_type: Base, entity_data: dict) -> bool:
        new_entity = entity_type(**entity_data)
        self.session.add(new_entity)
        return self.__commit_or_rollback()

    def update_entity(self, original_entity: Base, new_entity_data: dict) -> bool:
        for field_name, value in new_entity_data.items():
            if hasattr(original_entity, field_name):
                setattr(original_entity, field_name, value)
        return self.__commit_or_rollback()

    def delete_entity(self, entity: Base) -> bool:
        entity.status = Const.status_deleted
        return self.__commit_or_rollback()

    def __commit_or_rollback(self) -> bool:
        try:
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def get_customer(self, values: tuple | None) -> Customer | None:
        selected_customer = self.session.query(Customer).filter(
            Customer.first_name == values[1],
            Customer.last_name == values[2],
            or_(Customer.company_name == values[0], Customer.company_name.is_(None))
        ).first()

        if not selected_customer:
            return None

        return selected_customer

    def get_project_by_customer_id_and_name(self, customer_id: int, project_name: str) -> Project | None:
        return self.session.query(Project).filter_by(customer_id=customer_id, project_name=project_name).first()

    def delete_project_and_all_items(self, project: Project) -> bool:
        project.status = Const.status_deleted
        self.session.query(Item).filter(Item.project_id == project.project_id).update({'status': Const.status_deleted})
        return self.__commit_or_rollback()

    def get_user_settings(self) -> UserSettings | None:
        return self.session.query(UserSettings).first()

    def get_general_items(self) -> list | None:
        return self.session.query(Item).filter(Item.project_id.is_(None)).all()

    def get_active_general_items(self) -> list | None:
        return self.session.query(Item).filter(
            and_(
                Item.project_id.is_(None),
                Item.status == Const.status_active
            )
        ).all()

    def get_items_by_project_or_general(self, project_id: int) -> list | None:
        return self.session.query(Item).filter(or_(Item.project_id.is_(None), Item.project_id == project_id)).all()
