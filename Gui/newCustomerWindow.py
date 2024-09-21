
import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session

from Gui.dataValidation import DataValidation
from models import UserSettings, Customer


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

        self.labels = {
            'company_name': (str, 'Company Name'),
            'first_name': (str, 'First Name'),
            'last_name': (str, 'Last Name'),
            'street': (str, 'Street'),
            'street_number': (int, 'Street Number'),
            'city': (str, 'City'),
            'country': (str, 'Country'),
            'company_registration_number': (str, 'Company Registration Number')
        }

        self.entries = []
        self.create_window_objects()

    def create_window_objects(self):
        is_integer = (self.register(DataValidation.integer), '%P')

        for index, (name, definition) in enumerate(self.labels.items()):
            label = tk.Label(self, text=definition[1])
            label.grid(row=index + 1, column=0, padx=5, pady=5, sticky='W')
            should_validate_int = definition[0] == int
            entry = tk.Entry(
                self,
                width=50,
                validate='key',
                validatecommand=is_integer
            ) if should_validate_int else tk.Entry( self, width=50)

            entry.grid(row=index + 1, column=1, padx=5, pady=5)
            self.entries.append(entry)

        submit_button = tk.Button(self, text="Save and Close", command=self.submit)
        submit_button.grid(row=len(self.labels) + 1, column=0, columnspan=2, pady=20)

    def submit(self):
        customer_data = {field_name: entry.get() for field_name, entry in zip(self.labels.keys(), self.entries)}
        new_customer = Customer(**customer_data)
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
