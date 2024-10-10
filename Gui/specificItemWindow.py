import tkinter as tk
import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Item


class SpecificItemWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, entity_name: str, controller, operation: str):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.operation = operation
        self.title(WindowHelper.get_title(self.entity_name, operation))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.customers = self.controller.get_customers()
        self.customer_map = {}
        self.selected_customer = None
        self.selected_project = None
        self.selected_item = None
        self.items = None
        self.entries = []

        self.fields = {
            'item_name': (tk.StringVar(), 'Item Name'),
            'item_note': (tk.StringVar(), 'Item Note'),
            'item_price_per_unit': (ctk.StringVar(), 'Price per Unit'),
            'price_unit': (ctk.StringVar(), 'Price Unit')
        }

        self.create_window_objects()

    def create_window_objects(self) -> None:
        row = 0

        ctk.CTkLabel(self, text='Customer').grid(row=row, column=1, padx=0, pady=0, sticky='SW')
        row += 1

        self.customer_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_customer_select)
        self.customer_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
        row += 1

        ctk.CTkLabel(self, text='Project').grid(row=2, column=1, padx=0, pady=0, sticky='SW')
        row += 1

        self.project_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_project_select)
        self.project_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
        row += 1

        if self.operation == Const.op_edit:
            ctk.CTkLabel(self, text='Item').grid(row=4, column=1, padx=0, pady=0, sticky='SW')
            row += 1

            self.item_combobox = ctk.CTkComboBox(self, state="readonly", width=500, command=self.on_item_select)
            self.item_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
            row += 1

        last_key = list(self.fields)[-1]
        for name, (var, label_text) in self.fields.items():
            ctk.CTkLabel(self, text=label_text).grid(row=row, column=1, padx=0, pady=0, sticky='SW')
            row += 1

            if name != last_key:
                entry = ctk.CTkEntry(
                    self,
                    textvariable=var,
                    width=500, state='disabled' if self.operation == Const.op_edit else 'normal'
                )
                entry.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                self.entries.append(entry)
                row += 1
            else:
                self.price_unit_combobox = ctk.CTkComboBox(
                    self,
                    state='disabled' if self.operation == Const.op_edit else "readonly",
                    width=500,
                    command=self.on_price_unit_select
                )
                row += 1
                self.price_unit_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                row += 1

        ctk.CTkButton(
            self,
            text='Save Item and Close' if self.operation == Const.op_add else 'Update Item',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=row, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False, center=False)
        self.load_combo_customers()
        self.load_combo_price_units()

    def load_combo_customers(self) -> None:
        self.create_customer_map()
        customer_names = list(self.customer_map.keys())

        if customer_names:
            self.customer_combobox.set(customer_names[0])
            self.customer_combobox.configure(values=customer_names)
            self.on_customer_select()
        else:
            self.customer_combobox.configure(values=[''], state='disabled')
            self.clear_fields()
            self.disable_entries()

    def load_combo_price_units(self) -> None:
        price_units = list(Const.price_units.keys())
        self.price_unit_combobox.configure(values=price_units)
        self.price_unit_combobox.set(price_units[0])
        self.fields['price_unit'][0].set(price_units[0])

    def create_customer_map(self) -> None:
        for customer in self.customers:
            customer_name = (
                f'{customer.company_name + ", " if customer.company_name is not None else ""} '
                f'{customer.first_name} {customer.last_name}, '
                f'{customer.street} {str(customer.street_number)}, {customer.city}'
            )
            self.customer_map[customer_name] = customer

    def clear_fields(self) -> None:
        for var, _ in self.fields.values():
            var.set('')

    def disable_entries(self) -> None:
        for entry in self.entries:
            entry.configure(state='disabled')

    def on_customer_select(self, event=None) -> None:
        self.set_selected_customer()

        if self.selected_customer is not None:
            self.load_projects_for_selected_customer()

        if self.operation == Const.op_edit:
            self.item_combobox.set('')
            self.item_combobox.configure(values=[], state='disabled')
            self.selected_item = None
            self.clear_fields()

    def set_selected_customer(self) -> None:
        selected_customer_name = self.customer_combobox.get()
        self.selected_customer = self.customer_map[selected_customer_name]

    def load_projects_for_selected_customer(self) -> None:
        project_names = [project.project_name for project in self.selected_customer.projects]
        self.project_combobox.configure(values=project_names)

        if project_names:
            self.project_combobox.set(project_names[0])
            self.on_project_select()
        else:
            self.item_combobox.set('')
            self.item_combobox.configure(values=[], state='disabled')
            self.clear_fields()
            self.disable_entries()

    def on_project_select(self, event=None) -> None:
        self.set_selected_project()

        if self.selected_project is not None and self.operation == Const.op_edit:
            item_names = [item.item_name for item in self.selected_project.items]
            self.item_combobox.configure(values=item_names)

            if item_names and self.operation == Const.op_edit:
                self.item_combobox.configure(state='normal')
                self.item_combobox.set(item_names[0])
                self.on_item_select()
            else:
                self.item_combobox.set('')
                self.item_combobox.configure(values=[], state='disabled')
                self.clear_fields()
                self.disable_entries()

    def set_selected_project(self) -> None:
        selected_project_name = self.project_combobox.get()

        for project in self.selected_customer.projects:
            if project.project_name == selected_project_name:
                self.selected_project = project

        return None

    def on_item_select(self, event=None) -> None:
        self.set_selected_item()

        if self.selected_item:
            for key, (var, name) in self.fields.items():
                value = getattr(self.selected_item, key)
                var.set(value if value is not None else '')

            self.price_unit_combobox.configure(state='normal')
            self.price_unit_combobox.set(self.selected_item.price_unit)
            self.price_unit_combobox.configure(state='disabled')

            for entry in self.entries:
                entry.configure(state="normal")
        else:
            self.clear_fields()
            self.disable_entries()

    def set_selected_item(self) -> None:
        selected_item_name = self.item_combobox.get()

        for item in self.selected_project.items:
            if item.item_name == selected_item_name:
                self.selected_item = item

        return None

    def on_price_unit_select(self, event=None) -> None:
        value = self.price_unit_combobox.get()
        self.fields['price_unit'][0].set(value)

    def submit(self) -> None:
        validated_data = DataValidation.validate_data(Item, self.fields)

        if validated_data is None:
            return

        if self.selected_customer is None or self.selected_project is None:
            Message.common_one_button_msg(
                'fail', 'Invalid Input', 'Please select a customer and a project.'
            )
            return

        if self.operation == Const.op_edit:
            if self.selected_item is None:
                Message.common_one_button_msg('fail', 'Invalid Input', 'Please select an item.')
                return

            result = self.controller.update_item(self.selected_item, validated_data)
            Message.show_db_result(result, 'Item', self.selected_item)

        else:
            validated_data.update({'project_id': self.selected_project.project_id})
            result = self.controller.save_item(validated_data)
            Message.show_db_result(result, 'Item', None)

        self.grab_release()
        self.destroy()
