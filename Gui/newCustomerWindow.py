import tkinter as tk

from Gui.dataValidation import DataValidation
from Gui.windowDetails import WindowDetails
from models import Customer


class NewCustomerWindow(tk.Toplevel):

    def __init__(self, parent: tk.Tk, controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.label = tk.Label(self, text='New Customer')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.fields = {
            'company_name': (tk.StringVar(), 'Company Name'),
            'first_name': (tk.StringVar(), 'First Name'),
            'last_name': (tk.StringVar(), 'Last Name'),
            'street': (tk.StringVar(), 'Street'),
            'street_number': (tk.StringVar(), 'Street Number'),
            'city': (tk.StringVar(), 'City'),
            'country': (tk.StringVar(), 'Country'),
            'company_registration_number': (tk.StringVar(), 'Company Registration Number')
        }

        self.entries = []
        self.create_window_objects()

    def create_window_objects(self):
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            label = tk.Label(self, text=label_text)
            label.grid(row=index + 1, column=0, padx=5, pady=5, sticky='W')
            entry = tk.Entry(self, textvariable=var, width=50)
            entry.grid(row=index + 1, column=1, padx=5, pady=5)
            self.entries.append(entry)

        submit_button = tk.Button(self, text="Save and Close", command=self.submit)
        submit_button.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=20)

    def submit(self):
        validated_data = DataValidation.validate_data(Customer, self.fields)

        if validated_data is None:
            return

        self.controller.save_customer(validated_data)
        self.grab_release()
        self.destroy()
