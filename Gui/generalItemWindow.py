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
        self.general_items = self.controller.get_active_general_items()
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
        if self.mode == Const.mode_edit or self.mode == Const.mode_delete:
            ctk.CTkLabel(self, text='Item').grid(row=row, column=1, padx=0, pady=(20, 0), sticky='SW')
            row += 1

            self.general_item_combobox = ctk.CTkComboBox(
                self,
                state='readonly',
                width=300,
                command=self.on_item_select,
                values=[]
            )
            self.general_item_combobox.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
            row += 1

        last_key = list(self.fields)[-1]
        for name, (var, label_text) in self.fields.items():
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=row, column=1, padx=0, pady=(20 if row == 0 else 0, 0), sticky='SW')
            row += 1

            if name != last_key:
                entry = ctk.CTkEntry(
                    self,
                    textvariable=var,
                    width=300,
                    state='disabled' if self.mode == Const.mode_edit or self.mode == Const.mode_delete else 'normal'
                )
                entry.grid(row=row, column=1, padx=0, pady=(0, 15), sticky='NW')
                row += 1
                self.entries.append(entry)
            else:
                self.price_unit_combobox = ctk.CTkComboBox(
                    self,
                    state='disabled' if self.mode == Const.mode_edit or self.mode == Const.mode_delete else 'readonly',
                    width=300,
                    command=self.on_price_unit_select
                )
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
        self.load_combo_price_units()
        self.load_combo_general_items()

    def load_combo_price_units(self) -> None:
        price_units = [key for key in Const.price_units.keys() if key != 'hours']
        self.price_unit_combobox.configure(values=price_units)
        self.price_unit_combobox.set(price_units[0])
        self.fields['price_unit'][0].set(price_units[0])

    def load_combo_general_items(self) -> None:
        if self.mode in [Const.mode_edit, Const.mode_delete]:
            item_values = [item.item_name for item in self.general_items]
            self.general_item_combobox.configure(values=item_values if item_values else '')
            self.general_item_combobox.set('')

    def on_item_select(self, event=None) -> None:
        selected_item_name = self.general_item_combobox.get()
        self.selected_item = self.get_selected_item(selected_item_name)

        if self.selected_item is not None:
            self.populate_item_fields(self.selected_item)

        for entry in self.entries:
            if self.selected_item is None or self.mode == Const.mode_delete:
                entry.configure(state='disabled')
            else:
                entry.configure(state="normal")

        self.price_unit_combobox.configure(state='normal')
        self.price_unit_combobox.set(self.selected_item.price_unit)
        self.price_unit_combobox.configure(state='disabled')

    def get_selected_item(self, selected_item_name) -> Item | None:
        for item in self.general_items:
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
        if self.mode in [Const.mode_edit, Const.mode_delete] and self.selected_item is None:
            Message.common_one_button_msg(
                'fail',
                'Invalid Input',
                f'Please select an item to {self.mode}.'
            )
            return False

        return True

    def on_add(self, validated_data) -> bool:
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
