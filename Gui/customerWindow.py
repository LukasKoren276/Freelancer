import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Customer


class CustomerWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, entity_name: str, controller, mode: str, customer: Customer | None = None):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.mode = mode
        self.selected_customer = customer

        self.fields = {
            'company_name': (
                ctk.StringVar(value=self.selected_customer.company_name if self.selected_customer is not None else ''),
                'Company Name'
            ),
            'first_name': (
                ctk.StringVar(value=self.selected_customer.first_name if self.selected_customer is not None else ''),
                'First Name'
            ),
            'last_name': (
                ctk.StringVar(value=self.selected_customer.last_name if self.selected_customer is not None else ''),
                'Last Name'
            ),
            'street': (
                ctk.StringVar(value=self.selected_customer.street if self.selected_customer is not None else ''),
                'Street'
            ),
            'street_number': (
                ctk.StringVar(value=self.selected_customer.street_number if self.selected_customer is not None else ''),
                'Street Number'
            ),
            'city': (
                ctk.StringVar(value=self.selected_customer.city if self.selected_customer is not None else ''),
                'City'
            ),
            'country': (
                ctk.StringVar(value=self.selected_customer.country if self.selected_customer is not None else ''),
                'Country'
            ),
            'company_registration_number': (
                ctk.StringVar(
                    value=self.selected_customer.company_registration_number
                    if self.selected_customer is not None else ''
                ),
                'Company Registration Number'
            )
        }

        self.setup_window()
        self.create_window_objects()

    def setup_window(self):
        self.title(WindowHelper.get_title(self.entity_name, self.mode))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=20)

    def create_window_objects(self) -> None:
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=2 * index, column=1, padx=0, pady=(20 if index == 0 else 0, 0), sticky='SW')

            ctk.CTkEntry(
                self, textvariable=var, width=300, state='normal' if self.mode != Const.mode_delete else 'disabled'
            ).grid(row=2 * index + 1, column=1, padx=0, pady=(0, 15), sticky='NW')

        button_text = {
            Const.mode_add: 'Save Customer',
            Const.mode_edit: 'Update Customer',
            Const.mode_delete: 'Delete Customer'
        }.get(self.mode, 'Submit')

        ctk.CTkButton(
            self,
            text=button_text,
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=2 * len(self.fields) + 1, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False, center=False)

    def submit(self) -> None:
        validated_data = DataValidation.validate_data(Customer, self.fields)

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
            Message.show_db_result(result, 'Customer', self.mode)

        self.grab_release()
        self.destroy()

    def on_add(self, validated_data) -> bool:
        return self.controller.save_customer(validated_data)

    def on_edit(self, validated_data) -> bool:
        return self.controller.update_customer(self.selected_customer, validated_data)

    def on_delete(self) -> bool | None:
        msg_result = Message.show_msgbox(
            title='Do you really want to delete selected customer?',
            message='Once you delete the customer, it won\'t be available.',
            icon='warning',
            option_1=Const.yes,
            option_2=Const.no
        )

        if msg_result == Const.yes:
            return self.controller.delete_customer(self.selected_customer)
