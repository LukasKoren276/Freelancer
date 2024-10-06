import customtkinter as ctk

from helpers.dataValidation import DataValidation
from helpers.message import Message
from Gui.setup.windowDetails import WindowDetails
from models import Item


class GeneralItemWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, controller, window_details: WindowDetails, edit: bool = False):
        super().__init__(parent)
        self.controller = controller
        self.edit = edit
        self.title(window_details.title if not self.edit else 'Edit General Item')
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)

        self.fields = {
            'item_name': (ctk.StringVar(), 'Item Name'),
            'item_note': (ctk.StringVar(), 'Item Note'),
            'item_price_per_unit': (ctk.StringVar(), 'Price per Unit'),
            'price_unit': (ctk.StringVar(), 'Unit')
        }

        self.items = None
        self.selected_item = None
        self.entries = []
        self.create_window_objects()

    def create_window_objects(self):
        if self.edit:
            ctk.CTkLabel(self, text='Select Item to Edit').grid(row=0, column=1, padx=0, pady=0, sticky='SW')
            self.general_item_combobox = ctk.CTkComboBox(self, state="readonly", width=300, command=self.on_item_select)
            self.general_item_combobox.grid(row=1, column=1, padx=0, pady=(0, 15), sticky='NW')

        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=2 * index + 2, column=1, padx=0, pady=0, sticky='SW')

            entry = ctk.CTkEntry(self, textvariable=var, width=300, state='disabled' if self.edit else 'normal')
            entry.grid(row=2 * index + 3, column=1, padx=0, pady=(0, 15), sticky='NW')
            self.entries.append(entry)

        ctk.CTkButton(
            self,
            text='Save Item and Close' if not self.edit else 'Update Item',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=2 * len(self.fields) + 3, column=1, pady=40)

        self.load_combo_general_items()

    def load_combo_general_items(self) -> None:
        if self.edit:
            self.items = self.controller.get_general_items()
            item_values = [item.item_name for item in self.items]
            self.general_item_combobox.configure(values=item_values)

            if item_values:
                self.general_item_combobox.set(item_values[0])

    def on_item_select(self, event=None) -> None:
        self.selected_item = self.get_selected_item()

        for key, (var, name) in self.fields.items():
            var.set(getattr(self.selected_item, key))

        for entry in self.entries:
            entry.configure(state="normal")

    def get_selected_item(self) -> Item | None:
        for item in self.items:
            if item.item_name == self.general_item_combobox.get():
                return item

        return None

    def submit(self):
        validated_data = DataValidation.validate_data(Item, self.fields)

        if validated_data is None:
            return

        if self.edit:
            result = self.controller.update_item(self.selected_item, validated_data)
        else:
            result = self.controller.save_item(validated_data)

        Message.show_db_result(result, 'Item', self.selected_item)

        self.grab_release()
        self.destroy()
