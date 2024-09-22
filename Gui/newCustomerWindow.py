import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session

from Gui.dataValidation import DataValidation
from models import Customer


class NewCustomerWindow(tk.Toplevel):
    width = 500
    height = 550

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('Settings')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.label = tk.Label(self, text='New Customer')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.fields = {
            'company_name': (tk.StringVar(), 'Company Name'),
            'first_name': (tk.StringVar(), 'First Name'),
            'last_name': (tk.StringVar(), 'Last Name'),
            'street': (tk.StringVar(), 'Street'),
            'street_number': (tk.IntVar(), 'Street Number'),
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
        customer_data = {field_name: entry.get() for field_name, entry in zip(self.fields.keys(), self.entries)}

        if not DataValidation.is_data_valid(Customer, self.fields):
            return

        new_customer = Customer(**DataValidation.convert_empty_fields_to_null(customer_data))
        self.session.add(new_customer)

        try:
            self.session.commit()
            messagebox.showinfo('Success', 'Customer saved successfully!')
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save the customer: {e}')
            self.session.rollback()
        finally:
            self.grab_release()
            self.destroy()
