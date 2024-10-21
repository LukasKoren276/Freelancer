import customtkinter as ctk

from Gui.modeSelectionWindow import ModeSelectionWindow
from Gui.timeManagementWindow import TimeManagementWindow
from controllers.databaseManager import DatabaseManager
from Gui.customerSelectionWindow import CustomerSelectionWindow
from Gui.customerWindow import CustomerWindow
from Gui.generalItemWindow import GeneralItemWindow
from Gui.mainWindow import MainWindow
from Gui.settingsWindow import SettingsWindow
from Gui.specificItemWindow import SpecificItemWindow
from Gui.projectWindow import ProjectWindow
from helpers.constants import Constants as Const
from models import Customer, UserSettings, Project, Item, ItemTime


class GuiController:

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        self.main_window = None
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

    def open_main_window(self) -> None:
        self.main_window = MainWindow(Const.main_window, self)
        self.main_window.mainloop()

    def customer_management(self):
        result = self.__mode_selection_window(
            Const.customer_window,
            names=(Const.customer_window,),
            functions=(self.__customer_window,),
            modes=(Const.mode_add, Const.mode_edit, Const.mode_delete)
        )

        if result is not None:
            function, mode = result

            match mode:
                case Const.mode_add: self.__customer_window(mode)
                case Const.mode_edit | Const.mode_delete: self.__customer_selection(mode)

    def __customer_window(self, mode: str, customer: Customer = None) -> None:
        customer_window = CustomerWindow(self.main_window, Const.customer_window, self, mode, customer)
        customer_window.grab_set()

    def __customer_selection(self, mode: str) -> None:
        customer_selection_window = CustomerSelectionWindow(self.main_window, Const.customer_selection, self)
        customer_selection_window.grab_set()
        self.main_window.wait_window(customer_selection_window)
        customer = self.get_customer(customer_selection_window.get_customer_values())

        if customer is not None:
            self.__customer_window(mode, customer)

    def project_management(self):
        result = self.__mode_selection_window(
            Const.project_window,
            names=(Const.project_window,),
            functions=(self.__project_window,),
            modes=(Const.mode_add, Const.mode_edit, Const.mode_delete)
        )

        if result is not None:
            function, mode = result
            function(mode)

    def __project_window(self, mode: str) -> None:
        project_window = ProjectWindow(self.main_window, Const.project_window, self, mode=mode)
        project_window.grab_set()

    def item_management(self):
        result = self.__mode_selection_window(
            Const.item_window,
            names=(Const.general_item_window, Const.specific_item_window),
            functions=(self.__general_item_window, self.__specific_item_window),
            modes=(Const.mode_add, Const.mode_edit, Const.mode_delete)
        )

        if result is not None:
            function, mode = result
            function(mode)

    def __general_item_window(self, mode: str) -> None:
        item_window = GeneralItemWindow(self.main_window, Const.general_item_window, self, mode)
        item_window.grab_set()

    def __specific_item_window(self, mode: str):
        item_window = SpecificItemWindow(self.main_window, Const.specific_item_window, self, mode)
        item_window.grab_set()

    def __mode_selection_window(self, title, **kwargs) -> tuple | None:
        names = kwargs.get('names')
        functions = kwargs.get('functions')
        modes = kwargs.get('modes')

        if (names is not None or functions is not None or modes is not None) and len(names) == len(functions):
            selection_window = ModeSelectionWindow(self.main_window, self, title, names, functions, modes)

            selection_window.grab_set()
            self.main_window.wait_window(selection_window)
            function = selection_window.get_selected_function()
            mode = selection_window.get_selected_mode()

            if function is not None and mode is not None:
                return function, mode
        else:
            return None

    def time_management(self):
        time_management_window = TimeManagementWindow(self.main_window, self)
        time_management_window.grab_set()
        self.main_window.wait_window(time_management_window)

    def time_insertion_window(self, class_name, time_management_window, identifier):
        time_management_window.grab_release()
        time_management_window.withdraw()

        window = class_name(
            self.main_window,
            self,
            time_management_window,
            identifier,
        )
        window.grab_set()

    # TODO
    def create_offer(self):
        pass

    # TODO
    def create_invoice(self):
        pass

    def settings_window(self):
        settings_window = SettingsWindow(self.main_window, Const.settings_window, self)
        settings_window.grab_set()

    # DatabaseManager calls --------------------------------------------------------------------------------------------

    def get_customers(self) -> list | None:
        return self.db_manager.get_entities(Customer)

    def get_active_customers(self) -> list | None:
        return self.db_manager.get_active_entities(Customer)

    def get_customer(self, values: tuple | None) -> Customer | None:
        if values:
            return self.db_manager.get_customer(values)
        return None

    def save_customer(self, customer_data: dict) -> bool:
        return self.db_manager.save_entity(Customer, customer_data)

    def update_customer(self, original_customer: Customer, new_customer_data: dict) -> bool:
        return self.db_manager.update_entity(original_customer, new_customer_data)

    def delete_customer(self, customer: Customer) -> bool:
        return self.db_manager.delete_entity(customer)

    def get_projects(self) -> list | None:
        return self.db_manager.get_entities(Project)

    def get_active_projects(self) -> list | None:
        return self.db_manager.get_active_entities(Project)

    def get_project_by_customer_id_and_name(self, customer_id: int, project_name: str) -> Project | None:
        return self.db_manager.get_project_by_customer_id_and_name(customer_id, project_name)

    def save_project(self, project_data: dict) -> bool:
        return self.db_manager.save_entity(Project, project_data)

    def update_project(self, original_project: Project, project_data: dict) -> bool:
        return self.db_manager.update_entity(original_project, project_data)

    def delete_project(self, project: Project) -> bool:
        return self.db_manager.delete_entity(project)

    def delete_project_and_all_items(self, project: Project) -> bool:
        return self.db_manager.delete_project_and_all_items(project)

    def get_general_items(self) -> list | None:
        return self.db_manager.get_general_items()

    def get_active_general_items(self) -> list | None:
        return self.db_manager.get_active_general_items()

    def get_items_by_project_or_general(self, project_id: int) -> list | None:
        return self.db_manager.get_items_by_project_or_general(project_id)

    def save_item(self, item_data: dict) -> bool:
        return self.db_manager.save_entity(Item, item_data)

    def update_item(self, original_item: Item, item_data: dict) -> bool:
        return self.db_manager.update_entity(original_item, item_data)

    def delete_item(self, item: Item) -> bool:
        return self.db_manager.delete_entity(item)

    def save_item_time(self, item_time_data: dict) -> bool:
        return self.db_manager.save_entity(ItemTime, item_time_data)

    def get_user_settings(self) -> UserSettings | None:
        return self.db_manager.get_user_settings()

    def save_user_settings(self, user_settings_data: dict) -> bool:
        return self.db_manager.save_entity(UserSettings, user_settings_data)

    def update_user_settings(self, original_user_settings: UserSettings, user_settings_data: dict) -> bool:
        return self.db_manager.update_entity(original_user_settings, user_settings_data)
