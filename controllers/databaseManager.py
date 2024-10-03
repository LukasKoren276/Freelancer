import re
from tkinter import messagebox
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Customer, UserSettings, Base, Project, Price, Item


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def __get_entities(self, entity_type: Base) -> Base | None:
        return self.session.query(entity_type).all()

    def __save_entity(self, entity_type: Base, entity_data: dict) -> None:
        new_entity = entity_type(**entity_data)
        self.session.add(new_entity)
        self.__commit_or_rollback(new_entity.__class__.__name__)

    def __save_entity_and_return_entity(self, entity_type: Base, entity_data: dict) -> Base | None:
        new_entity = entity_type(**entity_data)
        self.session.add(new_entity)

        try:
            self.session.flush()
            return new_entity
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save {self.__split_camel_case(entity_type.__class__.__name__)} \n{e}"')
            self.session.rollback()
            return None

    def __update_entity(self, original_entity: Base, new_entity_data: dict) -> None:
        for field_name, value in new_entity_data.items():
            if hasattr(original_entity, field_name):
                setattr(original_entity, field_name, value)
        self.__commit_or_rollback(original_entity.__class__.__name__)

    def __commit_or_rollback(self, entity_name: str) -> None:
        try:
            self.session.commit()
            messagebox.showinfo('Success', f'{self.__split_camel_case(entity_name)} saved successfully!')
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save {self.__split_camel_case(entity_name)} \n{e}"')
            self.session.rollback()

    def __split_camel_case(self, string: str) -> str:
        return ' '.join(re.findall(r'[A-Z][a-z]*', string))

    def get_customers(self) -> list | None:
        return self.__get_entities(Customer)

    def get_customer(self, values: tuple | None) -> Customer | None:
        selected_customer = self.session.query(Customer).filter(
            Customer.first_name == values[1],
            Customer.last_name == values[2],
            or_(Customer.company_name == values[0], Customer.company_name.is_(None))
        ).first()

        if not selected_customer:
            messagebox.showerror('Error', 'Customer not found.')
            return None

        return selected_customer

    def save_customer(self, customer_data: dict) -> None:
        self.__save_entity(Customer, customer_data)

    def update_customer(self, original_customer: Customer, new_customer_data: dict) -> None:
        self.__update_entity(original_customer, new_customer_data)

    def get_customer_projects(self, customer_id: int):
        return self.session.query(Project).filter_by(customer_id=customer_id).all()

    def get_project_by_customer_id_and_name(self, customer_id: int, project_name: str) -> Project | None:
        return self.session.query(Project).filter_by(customer_id=customer_id, project_name=project_name).first()

    def save_project(self, project_data: dict) -> None:
        self.__save_entity(Project, project_data)

    def update_project(self, original_project, project_data):
        self.__update_entity(original_project, project_data)

    def get_user_settings(self) -> UserSettings | None:
        return self.session.query(UserSettings).first()

    def save_user_settings(self, user_settings_data: dict) -> None:
        self.__save_entity(UserSettings, user_settings_data)

    def update_user_settings(self, original_user_settings: UserSettings, user_settings_data: dict) -> None:
        self.__update_entity(original_user_settings, user_settings_data)

    def get_item_price(self, item_id) -> int | None:
        return self.session.query(Price).filter_by(item_id=item_id).first()

    def save_item_with_price(self, item_data, price_data):
        item = self.__save_entity_and_return_entity(Item, item_data)

        if item is None:
            return

        price_data.update({'item_id': item.item_id})
        self.__save_entity(Price, price_data)

