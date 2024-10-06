import customtkinter as ctk

from Gui.generalItemWindow import GeneralItemWindow
from Gui.projectItemWindow import ProjectItemWindow
from controllers.databaseManager import DatabaseManager
from Gui.mainWindow import MainWindow
from Gui.settingsWindow import SettingsWindow
from Gui.customerSelectionWindow import CustomerSelectionWindow
from Gui.customerWindow import CustomerWindow
from Gui.projectWindow import ProjectWindow
from Gui.setup.windowSetup import (
    main_window_setup,
    customer_window_setup,
    customer_selection_window_setup,
    settings_window_setup,
    project_window_setup,
    general_item_window_setup,
    project_item_window_setup,
)
from models import Customer, UserSettings, Project, Item


class GuiController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.main_window = None
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

    def open_main_window(self) -> None:
        self.main_window = MainWindow(self, main_window_setup)
        self.main_window.mainloop()

    def new_customer(self) -> None:
        customer_window = CustomerWindow(self.main_window, self, customer_window_setup, customer=None)
        customer_window.grab_set()

    def edit_customer(self) -> None:
        customer_selection_window = CustomerSelectionWindow(self.main_window, self, customer_selection_window_setup)
        customer_selection_window.grab_set()
        self.main_window.wait_window(customer_selection_window)
        customer = self.get_customer(customer_selection_window.get_customer_values())

        if customer is not None:
            customer_window = CustomerWindow(self.main_window, self, customer_window_setup, customer)
            customer_window.grab_set()

    def new_project(self) -> None:
        project_window = ProjectWindow(self.main_window, self, project_window_setup, edit=False)
        project_window.grab_set()

    def edit_project(self) -> None:
        project_window = ProjectWindow(self.main_window, self, project_window_setup, edit=True)
        project_window.grab_set()

    def new_general_item(self) -> None:
        project_window = GeneralItemWindow(self.main_window, self, general_item_window_setup, edit=False)
        project_window.grab_set()

    def edit_general_item(self) -> None:
        project_window = GeneralItemWindow(self.main_window, self, general_item_window_setup, edit=True)
        project_window.grab_set()




    #
    # def add_item(self):
    #     add_item_window = AddItemWindow(self.main_window, self, add_item_window_setup)
    #     add_item_window.grab_set()
    #
    # def open_item_details_window(self, customer=None, project=None, item=None):
    #     item_details = ItemDetailsWindow(self.main_window, self, item_details_window_setup, customer, project, item)
    #     item_details.grab_set()
    #
    # def add_specific_item(self):
    #     customer_project_selection_window = CustomerProjectSelectionWindow(
    #         self.main_window,
    #         self,
    #         customer_project_selection_window_setup,
    #         self.open_item_details_window
    #     )
    #
    #     customer_project_selection_window.grab_set()

    # def edit_item(self):
    #     edit_project_window = CustomerProjectSelectionWindow(
    #         self.main_window,
    #         self,
    #         customer_project_selection_window_setup,
    #         self.open_item_details_window()
    #     )
    #
    #     edit_project_window.grab_set()

    # TODO
    def edit_item(self):
        pass

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
    def open_settings(self):
        settings_window = SettingsWindow(self.main_window, self, settings_window_setup)
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
