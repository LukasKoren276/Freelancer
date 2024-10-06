import customtkinter as ctk

from helpers.dataValidation import DataValidation
from helpers.message import Message
from Gui.setup.windowDetails import WindowDetails
from models import Customer


class CustomerWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, controller, window_details: WindowDetails, customer: Customer | None = None):
        super().__init__(parent)
        self.controller = controller
        self.customer = customer
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, minsize=50)

        self.fields = {
            'company_name': (
                ctk.StringVar(value=self.customer.company_name if self.customer is not None else ''),
                'Company Name'
            ),
            'first_name': (
                ctk.StringVar(value=self.customer.first_name if self.customer is not None else ''),
                'First Name'
            ),
            'last_name': (
                ctk.StringVar(value=self.customer.last_name if self.customer is not None else ''),
                'Last Name'
            ),
            'street': (
                ctk.StringVar(value=self.customer.street if self.customer is not None else ''),
                'Street'
            ),
            'street_number': (
                ctk.StringVar(value=self.customer.street_number if self.customer is not None else ''),
                'Street Number'
            ),
            'city': (
                ctk.StringVar(value=self.customer.city if self.customer is not None else ''),
                'City'
            ),
            'country': (
                ctk.StringVar(value=self.customer.country if self.customer is not None else ''),
                'Country'
            ),
            'company_registration_number': (
                ctk.StringVar(value=self.customer.company_registration_number if self.customer is not None else ''),
                'Company Registration Number'
            )
        }

        self.create_window_objects()

    def create_window_objects(self):
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            ctk.CTkLabel(
                self, text=label_text
            ).grid(row=2 * index, column=1, padx=0, pady=0, sticky='SW')

            ctk.CTkEntry(
                self, textvariable=var, width=300
            ).grid(row=2 * index + 1, column=1, padx=0, pady=(0, 15), sticky='NW')

        ctk.CTkButton(
            self,
            text='Save Customer and Close' if self.customer is None else 'Update Customer',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=2 * len(self.fields) + 1, column=1, pady=40)

    def submit(self):
        validated_data = DataValidation.validate_data(Customer, self.fields)

        if validated_data is None:
            return

        if self.customer is None:
            result = self.controller.save_customer(validated_data)
        else:
            result = self.controller.update_customer(self.customer, validated_data)

        Message.show_db_result(result, 'Customer', self.customer)

        self.grab_release()
        self.destroy()
