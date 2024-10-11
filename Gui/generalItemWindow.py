import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Item


class GeneralItemWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, entity_name: str, controller, mode: str):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.mode = mode
        self.title(WindowHelper.get_title(self.entity_name, mode))
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
        row = 0
        if self.mode == Const.mode_edit:
            ctk.CTkLabel(self, text='Select Item to Edit').grid(row=row, column=1, padx=0, pady=0, sticky='SW')
            row += 1

            self.general_item_combobox = ctk.CTkComboBox(self, state="readonly", width=300, command=self.on_item_select)
            self.general_item_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
            row += 1

        last_key = list(self.fields)[-1]
        for name, (var, label_text) in self.fields.items():
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=row, column=1, padx=0, pady=0, sticky='SW')
            row += 1

            if name != last_key:
                entry = ctk.CTkEntry(
                    self,
                    textvariable=var,
                    width=300,
                    state='disabled' if self.mode == Const.mode_edit else 'normal'
                )
                entry.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                row += 1
                self.entries.append(entry)
            else:
                self.price_unit_combobox = ctk.CTkComboBox(
                    self,
                    state='disabled' if self.mode == Const.mode_edit else 'readonly',
                    width=300,
                    command=self.on_price_unit_select
                )
                self.price_unit_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                row += 1

        ctk.CTkButton(
            self,
            text='Save Item and Close' if self.mode == Const.mode_add else 'Update Item',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=row, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False, center=False)
        self.load_combo_price_units()
        self.load_combo_general_items()

    def load_combo_price_units(self) -> None:
        price_units = [key for key in Const.price_units.keys() if key != 'hours']
        self.price_unit_combobox.configure(values=price_units)
        self.price_unit_combobox.set(price_units[0])
        self.fields['price_unit'][0].set(price_units[0])

    def load_combo_general_items(self) -> None:
        if self.mode == Const.mode_edit:
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

        if self.mode == Const.mode_edit:
            result = self.controller.update_item(self.selected_item, validated_data)
        else:
            result = self.controller.save_item(validated_data)

        Message.show_db_result(result, 'Item', self.selected_item)

        self.grab_release()
        self.destroy()
