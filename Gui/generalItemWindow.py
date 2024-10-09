import customtkinter as ctk

from helpers.constants import Constants as const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from Gui.setup.windowDetails import WindowDetails
from models import Item


class GeneralItemWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, controller, window_details: WindowDetails, operation: str):
        super().__init__(parent)
        self.controller = controller
        self.window_details = window_details
        self.operation = operation
        self.title(window_details.get_title('General Item', self.operation))
        self.geometry(self.window_details.geometry)
        self.resizable(*self.window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.general_items = None
        self.selected_item = None
        self.entries = []

        self.fields = {
            'item_name': (ctk.StringVar(), 'Item Name'),
            'item_note': (ctk.StringVar(), 'Item Note'),
            'item_price_per_unit': (ctk.StringVar(), 'Price per Unit'),
            'price_unit': (ctk.StringVar(), 'Price Unit')
        }

        self.create_window_objects()

    def create_window_objects(self) -> None:
        if self.operation == const.op_edit:
            ctk.CTkLabel(self, text='Select Item to Edit').grid(row=0, column=1, padx=0, pady=0, sticky='SW')
            self.general_item_combobox = ctk.CTkComboBox(self, state="readonly", width=300, command=self.on_item_select)
            self.general_item_combobox.grid(row=1, column=1, padx=0, pady=(0, 15), sticky='NW')

        last_key = list(self.fields)[-1]
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=2 * index + 2, column=1, padx=0, pady=0, sticky='SW')

            if name != last_key:
                entry = ctk.CTkEntry(
                    self,
                    textvariable=var,
                    width=300,
                    state='disabled' if self.operation == const.op_edit else 'normal'
                )
                entry.grid(row=2 * index + 3, column=1, padx=0, pady=(0, 15), sticky='NW')
                self.entries.append(entry)
            else:
                self.price_unit_combobox = ctk.CTkComboBox(
                    self,
                    state='disabled' if self.operation == const.op_edit else 'readonly',
                    width=300,
                    command=self.on_price_unit_select
                )
                self.price_unit_combobox.grid(row=2 * index + 3, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkButton(
            self,
            text='Save Item and Close' if self.operation == const.op_add else 'Update Item',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=2 * len(self.fields) + 3, column=1, pady=40)

        self.load_combo_price_units()
        self.load_combo_general_items()

    def load_combo_price_units(self) -> None:
        price_units = list(self.window_details.price_units().keys())
        self.price_unit_combobox.configure(values=price_units)
        self.price_unit_combobox.set(price_units[0])
        self.fields['price_unit'][0].set(price_units[0])

    def load_combo_general_items(self) -> None:
        if self.operation == const.op_edit:
            self.general_items = self.controller.get_general_items()
            item_values = [item.item_name for item in self.general_items]
            self.general_item_combobox.configure(values=item_values)

            if item_values:
                self.general_item_combobox.set(item_values[0])

    def on_item_select(self, event=None) -> None:
        self.selected_item = self.get_selected_item()
        if self.selected_item is not None:
            for key, (var, name) in self.fields.items():
                value = getattr(self.selected_item, key)
                var.set(value if value is not None else '')

        self.price_unit_combobox.configure(state='normal')
        self.price_unit_combobox.set(self.selected_item.price_unit)
        self.price_unit_combobox.configure(state='disabled')

        for entry in self.entries:
            entry.configure(state="normal")

    def on_price_unit_select(self, event=None) -> None:
        value = self.price_unit_combobox.get()
        self.fields['price_unit'][0].set(value)

    def get_selected_item(self) -> Item | None:
        for item in self.general_items:
            if item.item_name == self.general_item_combobox.get():
                return item

        return None

    def submit(self) -> None:
        validated_data = DataValidation.validate_data(Item, self.fields)

        if validated_data is None:
            return

        if self.operation == const.op_edit:
            result = self.controller.update_item(self.selected_item, validated_data)
        else:
            result = self.controller.save_item(validated_data)

        Message.show_db_result(result, 'Item', self.selected_item)

        self.grab_release()
        self.destroy()
