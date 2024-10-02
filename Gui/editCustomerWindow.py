import tkinter as tk

from Gui.dataValidation import DataValidation
from Gui.windowDetails import WindowDetails
from models import Customer


class EditCustomerWindow(tk.Toplevel):

    def __init__(self, parent,  controller, window_details: WindowDetails, customer: Customer):
        super().__init__(parent)
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.customer = customer

        self.fields = {
            'company_name': (tk.StringVar(value=self.customer.company_name), 'Company Name'),
            'first_name': (tk.StringVar(value=self.customer.first_name), 'First Name'),
            'last_name': (tk.StringVar(value=self.customer.last_name), 'Last Name'),
            'street': (tk.StringVar(value=self.customer.street), 'Street'),
            'street_number': (tk.StringVar(value=self.customer.street_number), 'Street Number'),
            'city': (tk.StringVar(value=self.customer.city), 'City'),
            'country': (tk.StringVar(value=self.customer.country), 'Country'),
            'company_registration_number': (tk.StringVar(value=self.customer.company_registration_number), 'Company Registration Number')
        }

        self.create_window_objects()

    def create_window_objects(self):
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            label = tk.Label(self, text=label_text)
            label.grid(row=index + 1, column=0, padx=5, pady=5, sticky='W')
            entry = tk.Entry(self, textvariable=var, width=50)
            entry.grid(row=index + 1, column=1, padx=5, pady=5)

        submit_button = tk.Button(self, text="Save and Close", command=self.submit)
        submit_button.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=20)

    def submit(self):
        validated_data = DataValidation.validate_data(Customer, self.fields)

        if validated_data is None:
            return

        self.controller.update_customer(self.customer, validated_data)
        self.grab_release()
        self.destroy()
