import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session

from Gui.dataValidation import DataValidation
from models import Customer


class EditCustomerWindow(tk.Toplevel):
    width = 500
    height = 550

    def __init__(self, parent, session: Session, customer: Customer):
        super().__init__(parent)
        self.parent = parent
        self.title('Edit Customer')
        self.session = session
        self.customer = customer
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)

        self.fields = {
            'company_name': (tk.StringVar(value=customer.company_name), 'Company Name'),
            'first_name': (tk.StringVar(value=customer.first_name), 'First Name'),
            'last_name': (tk.StringVar(value=customer.last_name), 'Last Name'),
            'street': (tk.StringVar(value=customer.street), 'Street'),
            'street_number': (tk.StringVar(value=customer.street_number), 'Street Number'),
            'city': (tk.StringVar(value=customer.city), 'City'),
            'country': (tk.StringVar(value=customer.country), 'Country'),
            'company_registration_number': (tk.StringVar(value=customer.company_registration_number), 'Company Registration Number')
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

        for field_name, value in validated_data.items():
            setattr(self.customer, field_name, value)

        try:
            self.session.commit()
            messagebox.showinfo('Success', 'Customer updated successfully!')
            self.parent.refresh_list()  # Refresh customer list in the EditCustomerWindow
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to update the customer: {e}')
            self.session.rollback()
        finally:
            self.grab_release()
            self.destroy()
