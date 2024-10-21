import customtkinter as ctk

from Gui.timeMeasurementWindow import TimeMeasurementWindow
from Gui.timeSpentWindow import TimeSpentWindow
from helpers.constants import Constants as Const
from helpers.dateTimeHelper import DateTimeHelper
from helpers.windowHelper import WindowHelper
from models import Project, Item


class TimeManagementWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, controller):
        super().__init__(parent)
        self.controller = controller
        self.customers = self.controller.get_active_customers()
        self.customer_map = {}
        self.selected_customer = None
        self.selected_project = None
        self.selected_item = None
        self.entries = []
        self.buttons = []
        self.selected_time_assignment = None
        self.item_duration_sum = 0
        self.attributes("-topmost", True)

        self.setup_window()
        self.create_window_objects()

    def setup_window(self) -> None:
        self.title('Manage time for project items')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=50)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

    def create_window_objects(self) -> None:
        row = 0

        ctk.CTkLabel(self, text='Customer').grid(row=row, column=1, padx=0, pady=(20, 0), sticky='SW')
        row += 1

        self.customer_combobox = ctk.CTkComboBox(
            self,
            state="readonly",
            width=500,
            command=self.on_customer_select,
            values=[]
        )
        self.customer_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
        row += 1

        ctk.CTkLabel(self, text='Project').grid(row=row, column=1, padx=0, pady=0, sticky='SW')
        row += 1

        self.project_combobox = ctk.CTkComboBox(
            self,
            state="readonly",
            width=500,
            command=self.on_project_select,
            values=[]
        )
        self.project_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')

        button_add_spent_time = ctk.CTkButton(
            self,
            text='Add spent Time',
            command=lambda identifier=Const.add_spent_time: self.__run_next_window(identifier),
            font=ctk.CTkFont(family="Helvetica", size=15),
            state='disabled'
        )
        button_add_spent_time.grid(row=row, column=3, pady=(0, 15))
        self.buttons.append(button_add_spent_time)
        row += 1

        ctk.CTkLabel(self, text='Item').grid(row=row, column=1, padx=0, pady=0, sticky='SW')
        row += 1

        self.item_combobox = ctk.CTkComboBox(
            self,
            state="readonly",
            width=500,
            command=self.on_item_select,
            values=[]
        )
        self.item_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')

        button_measure_time = ctk.CTkButton(
            self,
            text='Measure Time',
            command=lambda identifier=Const.measure_time: self.__run_next_window(identifier),
            font=ctk.CTkFont(family="Helvetica", size=15),
            state='disabled'
        )
        button_measure_time.grid(row=row, column=3, pady=(0, 15))
        self.buttons.append(button_measure_time)
        row += 1

        self.description_label = ctk.CTkLabel(self, text='Selected Item:\t-')
        self.description_label.grid(row=row, column=1, columnspan=5, padx=0, pady=(20, 0), sticky='SW')
        row += 1

        self.time_label = ctk.CTkLabel(self, text='Recorded Time:\t-')
        self.time_label.grid(row=row, column=1, padx=0, pady=(20, 0), sticky='SW')

        WindowHelper.size_and_center(self, resiz=False)
        self.load_combo_customers()

    def load_combo_customers(self) -> None:
        self.create_customer_map()
        self.customer_combobox.configure(values=list(self.customer_map.keys()))
        self.customer_combobox.set('')

    def create_customer_map(self) -> None:
        for customer in self.customers:
            customer_name = (
                f'{customer.company_name + ", " if customer.company_name is not None else ""} '
                f'{customer.first_name} {customer.last_name}, '
                f'{customer.street} {str(customer.street_number)}, {customer.city}'
            )
            self.customer_map[customer_name] = customer

    def on_customer_select(self, event=None) -> None:
        self.selected_customer = self.customer_map[self.customer_combobox.get()]
        WindowHelper.reset_combobox(self.project_combobox)
        WindowHelper.reset_combobox(self.item_combobox)
        self.description_label.configure(text='Selected Item:\t-')
        self.time_label.configure(text='Recorded Time:\t-')
        self.change_button_status_to('disabled')

        if self.selected_customer is not None:
            self.load_projects_for_selected_customer()

    def load_projects_for_selected_customer(self) -> None:
        project_names = [
            project.project_name for project in self.selected_customer.projects if project.status == Const.status_active
        ]
        self.project_combobox.configure(values=project_names)

        if project_names:
            self.project_combobox.configure(values=project_names, state='readonly')

    def on_project_select(self, event=None) -> None:
        self.selected_project = self.get_selected_project(self.project_combobox.get())
        self.description_label.configure(text='Selected Item:\t-')
        self.time_label.configure(text='Recorded Time:\t-')
        self.change_button_status_to('disabled')

        if self.selected_project is not None:
            item_names = [
                item.item_name for item in self.selected_project.items
                if item.status == Const.status_active and item.price_unit == Const.hours
            ]
            WindowHelper.reset_combobox(self.item_combobox, item_names)

            if item_names:
                self.item_combobox.configure(state='readonly')

    def get_selected_project(self, selected_project_name: str) -> Project | None:
        for project in self.selected_customer.projects:
            if project.project_name == selected_project_name:
                return project

        return None

    def on_item_select(self, event=None) -> None:
        self.selected_item = self.get_selected_item(self.item_combobox.get())
        self.description_label.configure(text='Selected Item:\t'
                                              + self.text_customer()
                                              + f' *** {self.selected_project.project_name} '
                                                f'*** {self.selected_item.item_name}')
        self.set_item_duration_sum()
        self.time_label.configure(
            text='Recorded Time:\t ' + DateTimeHelper.convert_seconds_to_time_string(self.item_duration_sum)
        )
        self.change_button_status_to('normal')

    def get_selected_item(self, selected_item_name: str) -> Item | None:
        for item in self.selected_project.items:
            if item.item_name == selected_item_name:
                return item

        return None

    def change_button_status_to(self, status: str) -> None:
        for button in self.buttons:
            button.configure(state=status)

    def text_customer(self):
        return (
            f'{self.selected_customer.company_name if self.selected_customer.company_name is not None else ""}, '
            f'{self.selected_customer.first_name} {self.selected_customer.last_name}'
        )

    def set_item_duration_sum(self) -> None:
        self.item_duration_sum = sum(item_time.duration_seconds for item_time in self.selected_item.times)

    def __run_next_window(self, identifier) -> None:
        match identifier:
            case Const.add_spent_time:
                return self.controller.time_insertion_window(TimeSpentWindow, self, identifier)
            case Const.measure_time:
                return self.controller.time_insertion_window(TimeMeasurementWindow, self, identifier)
