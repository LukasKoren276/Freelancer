import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Project


class ProjectWindow(ctk.CTkToplevel):

    def __init__(self, parent, entity_name: str, controller, mode: str):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.mode = mode
        self.title(WindowHelper.get_title(self.entity_name, self.mode))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.customers = self.controller.get_customers()
        self.customer_map = {}
        self.selected_customer = None

        self.fields = {
            'project_name': (ctk.StringVar(), 'Project Name')
        }

        self.create_window_objects()

    def create_window_objects(self) -> None:
        ctk.CTkLabel(self, text='Customer').grid(row=0, column=1, padx=0, pady=0, sticky='SW')
        self.customer_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_customer_select)
        self.customer_combobox.grid(row=1, column=1, padx=0, pady=(0, 15), sticky='NW')

        if self.mode == Const.mode_edit:
            ctk.CTkLabel(self, text='Project').grid(row=2, column=1, padx=0, pady=0, sticky='SW')
            self.project_combobox = ctk.CTkComboBox(self, state="readonly", width=500)
            self.project_combobox.grid(row=3, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkLabel(
            self, text='New Project Name' if self.mode == Const.mode_edit else 'Project Name'
        ).grid(row=4, column=1, padx=0, pady=0, sticky='SW')

        ctk.CTkEntry(
            self, textvariable=self.fields.get('project_name')[0], width=500
        ).grid(row=5, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkButton(
            self,
            text='Save Project and Close' if self.mode == Const.mode_add else 'Update Project',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=6, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False, center=False)
        self.load_combo_customers()

    def load_combo_customers(self) -> None:
        self.create_customer_map()
        customer_names = list(self.customer_map.keys())
        self.customer_combobox.configure(values=customer_names)

        if customer_names:
            self.customer_combobox.set(customer_names[0])
            self.on_customer_select()

    def create_customer_map(self) -> None:
        for customer in self.customers:
            customer_name = (
                f'{customer.company_name + ", " if customer.company_name is not None else ""} '
                f'{customer.first_name} {customer.last_name}, '
                f'{customer.street} {str(customer.street_number)}, {customer.city}'
            )
            self.customer_map[customer_name] = customer

    def on_customer_select(self, event=None) -> None:
        self.set_selected_customer()
        if self.mode == Const.mode_edit:
            self.load_projects_for_selected_customer()

    def set_selected_customer(self) -> None:
        selected_customer_name = self.customer_combobox.get()
        self.selected_customer = self.customer_map[selected_customer_name]

    def load_projects_for_selected_customer(self):
        project_names = [project.project_name for project in self.selected_customer.projects]

        if not project_names:
            self.project_combobox.configure(values=[])
            self.project_combobox.set('')
        else:
            self.project_combobox.configure(values=project_names)
            self.project_combobox.set(project_names[0])

    def get_selected_project(self) -> Project | None:
        selected_project_name = self.project_combobox.get()

        for project in self.selected_customer.projects:
            if project.project_name == selected_project_name:
                return project

        return None

    def submit(self) -> None:
        validated_data = DataValidation.validate_data(Project, self.fields)

        if validated_data is None:
            return

        if not self.selected_customer:
            Message.common_one_button_msg('fail', 'Invalid Input', 'Please select a customer.')
            return

        if self.mode == Const.mode_edit:
            project = self.get_selected_project()

            if not project:
                Message.common_one_button_msg('fail', 'Invalid Input', 'Please select a  project.')
                return

            result = self.controller.update_project(project, validated_data)

        else:
            validated_data.update({'customer_id': self.selected_customer.customer_id})
            result = self.controller.save_project(validated_data)

        Message.show_db_result(result, 'Project', None)

        self.grab_release()
        self.destroy()
