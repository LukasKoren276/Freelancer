import customtkinter as ctk

from controllers.databaseManager import DatabaseManager
from Gui.customerSelectionWindow import CustomerSelectionWindow
from Gui.customerWindow import CustomerWindow
from Gui.generalItemWindow import GeneralItemWindow
from Gui.itemKindSelectionWindow import ItemKindSelectionWindow
from Gui.mainWindow import MainWindow
from Gui.settingsWindow import SettingsWindow
from Gui.specificItemWindow import SpecificItemWindow
from Gui.projectWindow import ProjectWindow
from helpers.constants import Constants as Const
from models import Customer, UserSettings, Project, Item


class GuiController:

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.main_window = None
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

    def open_main_window(self) -> None:
        self.main_window = MainWindow(Const.main_window, self)
        self.main_window.mainloop()

    def new_customer_window(self) -> None:
        customer_window = CustomerWindow(self.main_window, Const.customer_window, self, customer=None)
        customer_window.grab_set()

    def edit_customer_window(self) -> None:
        customer_selection_window = CustomerSelectionWindow(self.main_window, Const.customer_selection, self)
        customer_selection_window.grab_set()
        self.main_window.wait_window(customer_selection_window)
        customer = self.get_customer(customer_selection_window.get_customer_values())

        if customer is not None:
            customer_window = CustomerWindow(self.main_window, Const.customer_window, self, customer)
            customer_window.grab_set()

    def new_project_window(self) -> None:
        project_window = ProjectWindow(self.main_window, Const.project_window, self, operation=Const.op_add)
        project_window.grab_set()

    def edit_project_window(self) -> None:
        project_window = ProjectWindow(self.main_window, Const.project_window, self, operation=Const.op_edit)
        project_window.grab_set()

    def new_item_window(self) -> None:
        self.__new_or_edit_item(Const.op_add)

    def edit_item_window(self) -> None:
        self.__new_or_edit_item(Const.op_edit)

    def __new_or_edit_item(self, operation):
        item_kind_window = ItemKindSelectionWindow(
            self.main_window,
            Const.item_kind_selection,
            self,
            operation=operation
        )

        item_kind_window.grab_set()
        self.main_window.wait_window(item_kind_window)
        window_action = item_kind_window.get_selected_method()

        if window_action is not None:
            window_action(operation)

    def general_item_window(self, operation: str) -> None:
        item_window = GeneralItemWindow(self.main_window, Const.general_item_window, self, operation)
        item_window.grab_set()

    def specific_item_window(self, operation: str):
        item_window = SpecificItemWindow(self.main_window, Const.specific_item_window, self, operation)
        item_window.grab_set()

    # TODO
    def log_time(self):
        pass

    # TODO
    def create_offer(self):
        pass

    # TODO
    def create_invoice(self):
        pass

    # TODO
    def settings_window(self):
        settings_window = SettingsWindow(self.main_window, Const.settings_window, self)
        settings_window.grab_set()

    # DatabaseManager calls --------------------------------------------------------------------------------------------

    def get_customers(self) -> list | None:
        return self.db_manager.get_entities(Customer)

    def get_customer(self, values: tuple | None) -> Customer | None:
        if values:
            return self.db_manager.get_customer(values)
        return None

    def save_customer(self, customer_data: dict) -> bool:
        return self.db_manager.save_entity(Customer, customer_data)

    def update_customer(self, original_customer: Customer, new_customer_data: dict) -> bool:
        return self.db_manager.update_entity(original_customer, new_customer_data)

    def get_projects(self) -> list | None:
        return self.db_manager.get_entities(Project)

    def get_project_by_customer_id_and_name(self, customer_id: int, project_name: str) -> Project | None:
        return self.db_manager.get_project_by_customer_id_and_name(customer_id, project_name)

    def save_project(self, project_data: dict) -> bool:
        return self.db_manager.save_entity(Project, project_data)

    def update_project(self, original_project: Project, project_data: dict) -> bool:
        return self.db_manager.update_entity(original_project, project_data)

    def get_general_items(self) -> list | None:
        return self.db_manager.get_general_items()

    def get_items_by_project_or_general(self, project_id: int) -> list | None:
        return self.db_manager.get_items_by_project_or_general(project_id)

    def save_item(self, item_data: dict) -> bool:
        return self.db_manager.save_entity(Item, item_data)

    def update_item(self, original_item: Item, item_data: dict) -> bool:
        return self.db_manager.update_entity(original_item, item_data)

    def get_user_settings(self) -> UserSettings | None:
        return self.db_manager.get_user_settings()

    def save_user_settings(self, user_settings_data: dict) -> bool:
        return self.db_manager.save_entity(UserSettings, user_settings_data)

    def update_user_settings(self, original_user_settings: UserSettings, user_settings_data: dict) -> bool:
        return self.db_manager.update_entity(original_user_settings, user_settings_data)
