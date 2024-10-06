import tkinter as tk
import customtkinter as ctk

from helpers.dataValidation import DataValidation
from helpers.message import Message
from Gui.setup.windowDetails import WindowDetails
from models import Project, Customer, Item

# TODO - DO NOT DELETE, only finish the logic
class ProjectItemWindow(ctk.CTkToplevel):

    def __init__(self, parent,  controller, window_details: WindowDetails, edit: bool = False):
        super().__init__(parent)
        self.controller = controller
        self.edit = edit
        self.title(window_details.title if not self.edit else 'Edit Item')
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.customers = self.controller.get_customers()
        self.customer_map = {}

        self.fields = {
            'item_name': (tk.StringVar(), 'Item Name'),
            'item_note': (tk.StringVar(), 'Item Note')
        }

        self.create_window_objects()

    def create_window_objects(self):
        ctk.CTkLabel(self, text='Customer').grid(row=0, column=1, padx=0, pady=0, sticky='SW')
        self.customer_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_customer_select)
        self.customer_combobox.grid(row=1, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkLabel(self, text='Project').grid(row=2, column=1, padx=0, pady=0, sticky='SW')
        self.project_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_project_select)
        self.project_combobox.grid(row=3, column=1, padx=0, pady=(0, 15), sticky='NW')

        if self.edit:
            ctk.CTkLabel(self, text='Item').grid(row=4, column=1, padx=0, pady=0, sticky='SW')
            self.item_combobox = ctk.CTkComboBox(self, state="readonly", width=500)
            self.item_combobox.grid(row=5, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkLabel(
            self, text='New Item Name' if self.edit else 'Item Name'
        ).grid(row=6, column=1, padx=0, pady=0, sticky='W')

        ctk.CTkEntry(
            self, textvariable=self.fields.get('item_name')[0], width=500
        ).grid(row=7, column=1, padx=0, pady=(0, 15))

        ctk.CTkLabel(
            self, text='New Item Note' if self.edit else 'Item Note'
        ).grid(row=8, column=1, padx=0, pady=0, sticky='W')

        ctk.CTkEntry(
            self, textvariable=self.fields.get('item_note')[0], width=500
        ).grid(row=9, column=1, padx=0, pady=(0, 15))

        ctk.CTkButton(
            self,
            text='Save Item and Close' if not self.edit else 'Update Item',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=10, column=1, pady=40)

        self.load_combo_customers()

    def load_combo_customers(self):
        self.create_customer_map()
        customer_names = list(self.customer_map.keys())
        self.customer_combobox.configure(values=customer_names)

        if customer_names:
            self.customer_combobox.set(customer_names[0])
            self.on_customer_select()

    def create_customer_map(self):
        for customer in self.customers:
            customer_name = (
                f'{customer.company_name + ", " if customer.company_name is not None else ""} '
                f'{customer.first_name} {customer.last_name}, '
                f'{customer.street} {str(customer.street_number)}, {customer.city}'
            )
            self.customer_map[customer_name] = customer

    def on_customer_select(self, event=None):
        self.load_projects_for_selected_customer(self.get_selected_customer())

    def get_selected_customer(self) -> Customer | None:
        selected_customer_name = self.customer_combobox.get()
        return self.customer_map[selected_customer_name]

    def load_projects_for_selected_customer(self, customer):
        project_names = [project.project_name for project in customer.projects]
        self.project_combobox.configure(values=project_names)

        if project_names:
            self.project_combobox.set(project_names[0])

    def get_selected_project(self, selected_customer: Customer) -> Project | None:
        selected_project_name = self.project_combobox.get()

        for project in selected_customer.projects:
            if project.project_name == selected_project_name:
                return project

        return None

    def get_selected_item(self, selected_project: Project) -> Project | None:
        selected_item_name = self.item_combobox.get()

        for item in selected_project.items:
            if item.item_name == selected_item_name:
                return item

        return None

    def on_project_select(self, event=None):
        project = self.get_selected_project(self.get_selected_customer())
        item_names = [item.item_name for item in project.items]

        if item_names and self.edit:
            self.item_combobox.set(item_names[0])

    def submit(self):
        validated_data = DataValidation.validate_data(Item, self.fields)

        if validated_data is None:
            return

        selected_customer = self.get_selected_customer()

        if not selected_customer:
            Message.common_one_buttton_msg('fail', 'Invalid Input', 'Please select a customer.')
            return

        project = self.get_selected_project(selected_customer)

        if not project:
            Message.common_one_buttton_msg('fail', 'Invalid Input', 'Please select a  project.')
            return

        if self.edit:
            item = self.get_selected_item(project)

            if not item:
                Message.common_one_buttton_msg('fail', 'Invalid Input', 'Please select an item.')
                return

            result = self.controller.update_item(item, validated_data)
            Message.show_db_result(result, 'Project', project)

        else:
            validated_data.update({'project_id': project.project_id})
            result = self.controller.save_item(validated_data)  # TODO add prices, units (hour, piece), create methods

        Message.show_db_result(result, 'Project', None)

        self.grab_release()
        self.destroy()
