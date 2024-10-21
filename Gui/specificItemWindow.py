import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Item, Project


class SpecificItemWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, entity_name: str, controller, mode: str):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.mode = mode
        self.customers = self.controller.get_active_customers()
        self.customer_map = {}
        self.selected_customer = None
        self.selected_project = None
        self.selected_item = None
        self.entries = []

        self.fields = {
            'item_name': (ctk.StringVar(), 'Item Name'),
            'item_note': (ctk.StringVar(), 'Item Note'),
            'item_price_per_unit': (ctk.StringVar(), 'Price per Unit'),
            'price_unit': (ctk.StringVar(), 'Price Units')
        }

        self.setup_window()
        self.create_window_objects()

    def setup_window(self) -> None:
        self.title(WindowHelper.get_title(self.entity_name, self.mode))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

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

        ctk.CTkLabel(self, text='Project').grid(row=2, column=1, padx=0, pady=0, sticky='SW')
        row += 1

        self.project_combobox = ctk.CTkComboBox(
            self,
            state="readonly",
            width=500,
            command=self.on_project_select,
            values=[]
        )
        self.project_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
        row += 1

        if self.mode in [Const.mode_edit, Const.mode_delete]:
            ctk.CTkLabel(self, text='Item').grid(row=4, column=1, padx=0, pady=0, sticky='SW')
            row += 1

            self.item_combobox = ctk.CTkComboBox(
                self,
                state="readonly",
                width=500,
                command=self.on_item_select,
                values=[]
            )
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
                    width=500, state='disabled' if self.mode in [Const.mode_edit, Const.mode_delete] else 'normal'
                )
                entry.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                self.entries.append(entry)
                row += 1
            else:
                self.price_unit_combobox = ctk.CTkComboBox(
                    self,
                    state='disabled' if self.mode in [Const.mode_edit, Const.mode_delete] else "readonly",
                    width=500,
                    command=self.on_price_unit_select
                )
                row += 1
                self.price_unit_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                row += 1

        button_text = {
            Const.mode_add: 'Save Item',
            Const.mode_edit: 'Update Item',
            Const.mode_delete: 'Delete Item'
        }.get(self.mode, 'Submit')

        ctk.CTkButton(
            self,
            text=button_text,
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=row, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False)
        self.load_combo_customers()
        self.load_combo_price_units()

    def load_combo_customers(self) -> None:
        self.create_customer_map()
        self.customer_combobox.configure(values=list(self.customer_map.keys()))
        self.customer_combobox.set('')

    def load_combo_price_units(self) -> None:
        self.price_unit_combobox.configure(values=list(Const.price_units.keys()))
        self.price_unit_combobox.set('')

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
        self.clear_fields()
        WindowHelper.reset_combobox(self.project_combobox)

        if self.mode != Const.mode_add:
            WindowHelper.reset_combobox(self.item_combobox)

        if self.selected_customer is not None:
            self.load_projects_for_selected_customer()

    def load_projects_for_selected_customer(self) -> None:
        project_names = [
            project.project_name for project in self.selected_customer.projects if project.status == Const.status_active
        ]
        self.project_combobox.configure(values=project_names)

        if project_names:
            self.project_combobox.configure(values=project_names, state='readonly')
        else:
            self.disable_entries()

    def on_project_select(self, event=None) -> None:
        self.selected_project = self.get_selected_project(self.project_combobox.get())
        self.clear_fields()

        if self.selected_project is not None:
            if self.mode in [Const.mode_edit, Const.mode_delete]:
                item_names = [
                    item.item_name for item in self.selected_project.items if item.status == Const.status_active
                ]
                WindowHelper.reset_combobox(self.item_combobox, item_names)

                if item_names:
                    self.item_combobox.configure(state='readonly')
                else:
                    self.disable_entries()

            if self.mode == Const.mode_add:
                self.enable_entries()
                self.clear_fields()

    def get_selected_project(self, selected_project_name: str) -> Project | None:
        for project in self.selected_customer.projects:
            if project.project_name == selected_project_name:
                return project

        return None

    def on_item_select(self, event=None) -> None:
        self.selected_item = self.get_selected_item(self.item_combobox.get())

        if self.selected_item is not None:
            self.populate_item_fields(self.selected_item)
            self.price_unit_combobox.configure(state='readonly')
            self.price_unit_combobox.set(self.selected_item.price_unit)
            self.price_unit_combobox.configure(state='disabled')

            for entry in self.entries:
                entry.configure(state='normal' if self.mode == Const.mode_edit else 'disabled')

    def get_selected_item(self, selected_item_name: str) -> Item | None:
        for item in self.selected_project.items:
            if item.item_name == selected_item_name:
                return item

        return None

    def populate_item_fields(self, selected_item: Item) -> None:
        for key, (var, name) in self.fields.items():
            value = getattr(selected_item, key)
            var.set(value if value is not None else '')

    def on_price_unit_select(self, event=None) -> None:
        value = self.price_unit_combobox.get()
        self.fields['price_unit'][0].set(value)

    def clear_fields(self) -> None:
        for (var, _) in self.fields.values():
            var.set('')

    def disable_entries(self) -> None:
        for entry in self.entries:
            entry.configure(state='disabled')

    def enable_entries(self) -> None:
        for entry in self.entries:
            entry.configure(state='normal')

    def submit(self) -> None:
        if not self.validate_selection():
            return

        validated_data = DataValidation.validate_data(Item, self.fields) if self.mode != Const.mode_delete else ''

        if validated_data is None:
            return

        match self.mode:
            case Const.mode_add:
                result = self.on_add(validated_data)
            case Const.mode_edit:
                result = self.on_edit(validated_data)
            case Const.mode_delete:
                result = self.on_delete()
            case _:
                raise ValueError('Mode not recognised.')

        if result is not None:
            Message.show_db_result(result, 'Item', self.mode)

        self.grab_release()
        self.destroy()

    def validate_selection(self) -> bool:
        if self.selected_customer is None or self.selected_project is None:
            Message.common_one_button_msg(
                'fail',
                'Invalid Input',
                'Please select a customer and a project.'
            )
            return False

        if self.mode in [Const.mode_edit, Const.mode_delete] and self.selected_item is None:
            Message.common_one_button_msg(
                'fail',
                'Invalid Input',
                f'Please select an item to {self.mode}.'
            )
            return False

        return True

    def on_add(self, validated_data) -> bool:
        validated_data['project_id'] = self.selected_project.project_id
        return self.controller.save_item(validated_data)

    def on_edit(self, validated_data) -> bool:
        return self.controller.update_item(self.selected_item, validated_data)

    def on_delete(self) -> bool | None:
        msg_result = Message.show_msgbox(
            title='Do you really want to delete selected item?',
            message='Once you delete the item, it won\'t be available.',
            icon='warning',
            option_1=Const.yes,
            option_2=Const.no
        )

        if msg_result == Const.yes:
            return self.controller.delete_item(self.selected_item)
