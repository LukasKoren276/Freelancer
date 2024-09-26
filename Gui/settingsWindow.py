import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from models import UserSettings
from Gui.dataValidation import DataValidation


class SettingsWindow(tk.Toplevel):
    width = 500
    height = 550

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('Settings')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.label = tk.Label(self, text='Settings')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.fields = {
            'user_first_name': (tk.StringVar(), 'First Name'),
            'user_last_name': (tk.StringVar(), 'Last Name'),
            'user_street': (tk.StringVar(), 'Street'),
            'user_street_number': (tk.StringVar(), 'Street Number'),
            'user_city': (tk.StringVar(), 'City'),
            'user_country': (tk.StringVar(), 'Country'),
            'company_name': (tk.StringVar(), 'Company Name'),
            'user_company_registration_number': (tk.StringVar(), 'Company Registration Number'),
            'user_registered_as': (tk.StringVar(), 'User Registered As'),
            'invoice_due_date': (tk.StringVar(), 'Invoice Due Date [days]'),
            'rate_per_hour': (tk.StringVar(), 'Rate Per Hour'),
            'currency': (tk.StringVar(), 'Currency'),
            'vat': (tk.StringVar(), 'VAT [%]')
        }

        self.load_user_settings()
        self.create_window_objects()

    def load_user_settings(self):
        user_settings = self.session.query(UserSettings).first()

        if user_settings:
            for field_name, (var, _) in self.fields.items():
                value = getattr(user_settings, field_name, None)

                if value is not None:
                    var.set(value)

    def create_window_objects(self):
        for index, (field_name, (var, label_text)) in enumerate(self.fields.items()):
            label = tk.Label(self, text=label_text)
            label.grid(row=index + 1, column=0, padx=5, pady=5, sticky='W')
            entry = tk.Entry(self, textvariable=var, width=50)
            entry.grid(row=index + 1, column=1, padx=5, pady=5)

        save_and_close_button = tk.Button(self, text="Save and Close", command=self.save_and_close_window)
        save_and_close_button.grid(row=14, column=0, columnspan=2, padx=5, pady=50)

    def save_and_close_window(self):
        user_settings = self.session.query(UserSettings).first()
        validated_data = DataValidation.validate_data(UserSettings, self.fields)

        if validated_data is None:
            return

        if not user_settings:
            user_settings = UserSettings(**validated_data)
            self.session.add(user_settings)
        else:
            for field_name, value in validated_data.items():
                setattr(user_settings, field_name, value)

        try:
            self.session.commit()
            messagebox.showinfo('Success', 'User settings saved successfully!')
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save user settings: {e}')
            self.session.rollback()
        finally:
            self.grab_release()
            self.destroy()
