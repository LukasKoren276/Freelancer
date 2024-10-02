from Gui.editProjectNameWindow import EditProjectNameWindow
from Gui.settingsWindow import SettingsWindow
from Gui.mainWindow import MainWindow
from Gui.addItemWindow import AddItemWindow
from Gui.customerSelectionWindow import CustomerSelectionWindow
from Gui.editCustomerWindow import EditCustomerWindow
from Gui.editProjectWindow import EditProjectWindow
from Gui.newCustomerWindow import NewCustomerWindow
from Gui.newPojectWindow import NewProjectWindow
from Gui.windowSetup import (
    main_window_setup,
    new_customer_window_setup,
    customer_selection_window_setup,
    edit_customer_window_setup,
    settings_window_setup,
    new_project_window_setup,
    edit_project_window_setup,
    edit_project_name_window_setup
)
from controllers.databaseManager import DatabaseManager
from models import Customer, UserSettings, Project


class GuiController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.main_window = None

    def open_main_window(self) -> None:
        self.main_window = MainWindow(self, main_window_setup)
        self.main_window.mainloop()

    def new_customer(self) -> None:
        new_customer_window = NewCustomerWindow(self.main_window, self, new_customer_window_setup)
        new_customer_window.grab_set()

    def edit_customer(self):
        customer = self.open_customer_selection(self.main_window)
        EditCustomerWindow(self.main_window, self, edit_customer_window_setup, customer)

    def open_customer_selection(self, parent_window) -> Customer | None:
        customer_selection_window = CustomerSelectionWindow(parent_window, self, customer_selection_window_setup)
        parent_window.wait_window(customer_selection_window)
        selected_customer = self.get_customer(customer_selection_window.get_customer_values())

        if selected_customer:
            return selected_customer

        return None

    def new_project(self):
        NewProjectWindow(self.main_window, self, new_project_window_setup)

    # TODO
    def edit_project(self) -> None:
        edit_project_window = EditProjectWindow(self.main_window, self, edit_project_window_setup)
        edit_project_window.grab_set()

    def edit_project_name(self, customer: Customer, project: Project) -> None:
        EditProjectNameWindow(self.main_window, self, edit_project_name_window_setup, customer, project)

    # TODO
    def add_item(self):
        add_item_window = AddItemWindow(self)
        add_item_window.grab_set()

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
        return self.db_manager.get_customers()

    def get_customer(self, values: tuple | None) -> Customer | None:
        if values:
            return self.db_manager.get_customer(values)
        return None

    def save_customer(self, customer_data: dict) -> None:
        self.db_manager.save_customer(customer_data)

    def update_customer(self, original_customer: Customer, new_customer_data: dict) -> None:
        self.db_manager.update_customer(original_customer, new_customer_data)

    def get_customer_projects(self, customer_id: int) -> list | None:
        return self.db_manager.get_customer_projects(customer_id)

    def get_project_by_customer_id_and_name(self, customer_id: int, project_name: str) -> Project | None:
        return self.db_manager.get_project_by_customer_id_and_name(customer_id, project_name)

    def save_project(self, project_data: dict) -> None:
        self.db_manager.save_project(project_data)

    def update_project(self, original_project: Project, project_data: dict) -> None:
        self.db_manager.update_project(original_project, project_data)

    def get_user_settings(self) -> UserSettings | None:
        return self.db_manager.get_user_settings()

    def save_user_settings(self, user_settings_data: dict) -> None:
        self.db_manager.save_user_settings(user_settings_data)

    def update_user_settings(self, original_user_settings: UserSettings, user_settings_data: dict) -> None:
        self.db_manager.update_user_settings(original_user_settings, user_settings_data)
