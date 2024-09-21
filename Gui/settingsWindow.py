
import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session

from models import UserSettings


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
        self.columnconfigure(0, weight=1)  # Ensure column 0 takes available space
        self.columnconfigure(1, weight=1)
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.street_number_var = tk.IntVar()
        self.city_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.company_registration_number_var = tk.StringVar()
        self.registered_as_var = tk.StringVar()
        self.invoice_due_date_var = tk.IntVar()
        self.rate_per_hour_var = tk.IntVar()
        self.currency_var = tk.StringVar()
        self.vat_var = tk.IntVar()
        self.load_user_settings()
        self.create_window_objects()

    def load_user_settings(self):
        user_settings = self.session.query(UserSettings).first()

        if user_settings:
            self.first_name_var.set(user_settings.user_first_name)
            self.last_name_var.set(user_settings.user_last_name)
            self.street_var.set(user_settings.user_street)
            self.street_number_var.set(user_settings.user_street_number)
            self.city_var.set(user_settings.user_city)
            self.country_var.set(user_settings.user_country)
            self.company_registration_number_var.set(user_settings.user_company_registration_number)
            self.registered_as_var.set(user_settings.user_registered_as)
            self.invoice_due_date_var.set(user_settings.invoice_due_date)
            self.rate_per_hour_var.set(user_settings.rate_per_hour)
            self.currency_var.set(user_settings.currency)
            self.vat_var.set(user_settings.vat)

    def create_window_objects(self):
        is_integer = (self.register(self.integer), '%P')
        is_integer_or_empty = (self.register(self.integer_or_empty), '%P')

        text_first_name = tk.Label(self, text='First Name')
        text_first_name.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        entry_first_name = tk.Entry(self, textvariable=self.first_name_var, width=50)
        entry_first_name.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        text_last_name = tk.Label(self, text='Last Name')
        text_last_name.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        entry_last_name = tk.Entry(self, textvariable=self.last_name_var, width=50)
        entry_last_name.grid(row=2, column=1, padx=5, pady=5, sticky="W")

        text_street = tk.Label(self, text='Street')
        text_street.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        entry_street = tk.Entry(self, textvariable=self.street_var, width=50)
        entry_street.grid(row=3, column=1, padx=5, pady=5, sticky="W")

        text_street_number = tk.Label(self, text='Street Number')
        text_street_number.grid(row=4, column=0, padx=5, pady=5, sticky="W")
        entry_street_number = tk.Entry(
            self,
            textvariable=self.street_number_var,
            width=50,
            validate='key',
            validatecommand=is_integer
        )
        entry_street_number.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        text_city = tk.Label(self, text='City')
        text_city.grid(row=5, column=0, padx=5, pady=5, sticky="W")
        entry_city = tk.Entry(self, textvariable=self.city_var, width=50)
        entry_city.grid(row=5, column=1, padx=5, pady=5, sticky="W")

        text_country = tk.Label(self, text='Country')
        text_country.grid(row=6, column=0, padx=5, pady=5, sticky="W")
        entry_country = tk.Entry(self, textvariable=self.country_var, width=50)
        entry_country.grid(row=6, column=1, padx=5, pady=5, sticky="W")

        text_company_reg_number = tk.Label(self, text='Company Registration Number')
        text_company_reg_number.grid(row=7, column=0, padx=5, pady=5, sticky="W")
        entry_company_reg_number = tk.Entry(self, textvariable=self.company_registration_number_var, width=50)
        entry_company_reg_number.grid(row=7, column=1, padx=5, pady=5, sticky="W")

        text_user_registered_as = tk.Label(self, text='User Registered As')
        text_user_registered_as.grid(row=8, column=0, padx=5, pady=5, sticky="W")
        entry_user_registered_as = tk.Entry(self, textvariable=self.registered_as_var, width=50)
        entry_user_registered_as.grid(row=8, column=1, padx=5, pady=5, sticky="W")

        text_invoice_due_date = tk.Label(self, text='Invoice Due Date [days]')
        text_invoice_due_date.grid(row=9, column=0, padx=5, pady=5, sticky="W")
        entry_invoice_due_date = tk.Entry(
            self,
            textvariable=self.invoice_due_date_var,
            width=50,
            validate='key',
            validatecommand=is_integer
        )
        entry_invoice_due_date.grid(row=9, column=1, padx=5, pady=5, sticky="W")

        text_rate_per_hour = tk.Label(self, text='Rate Per Hour')
        text_rate_per_hour.grid(row=10, column=0, padx=5, pady=5, sticky="W")
        entry_rate_per_hour = tk.Entry(
            self,
            textvariable=self.rate_per_hour_var,
            width=50,
            validate='key',
            validatecommand=is_integer
        )
        entry_rate_per_hour.grid(row=10, column=1, padx=5, pady=5, sticky="W")

        text_currency = tk.Label(self, text='Currency')
        text_currency.grid(row=11, column=0, padx=5, pady=5, sticky="W")
        entry_currency = tk.Entry(self, textvariable=self.currency_var, width=50)
        entry_currency.grid(row=11, column=1, padx=5, pady=5, sticky="W")

        text_vat = tk.Label(self, text='VAT [%]')
        text_vat.grid(row=12, column=0, padx=5, pady=5, sticky="W")
        entry_vat = tk.Entry(
            self,
            textvariable=self.vat_var,
            width=50,
            validate='key',
            validatecommand=is_integer_or_empty
        )
        entry_vat.grid(row=12, column=1, padx=5, pady=5, sticky="W")

        close_and_save_button = tk.Button(self, text="Save and Close", command=self.close_and_save_window)
        close_and_save_button.grid(row=13, column=0, columnspan=2, padx=5, pady=50)

    @staticmethod
    def integer(new_value):
        if new_value.isdigit():
            return True

        messagebox.showerror(
            'Invalid Input',
            'Please enter only numeric values.'
        )
        return False

    @staticmethod
    def integer_or_empty(new_value):
        if new_value == "" or new_value.isdigit():
            return True

        messagebox.showerror(
            'Invalid Input',
            'Please enter only numeric values or keep the field empty.'
        )
        return False

    def close_and_save_window(self):
        user_settings = self.session.query(UserSettings).first()

        if not user_settings:
            user_settings = UserSettings(
                user_first_name=self.first_name_var.get(),
                user_last_name=self.last_name_var.get(),
                user_company_registration_number=self.company_registration_number_var.get(),
                user_street=self.street_var.get(),
                user_street_number=self.street_number_var.get(),
                user_city=self.city_var.get(),
                user_country=self.country_var.get(),
                user_registered_as=self.registered_as_var.get(),
                invoice_due_date=self.invoice_due_date_var.get(),
                rate_per_hour=self.rate_per_hour_var.get(),
                currency=self.currency_var.get(),
                vat=self.vat_var.get()
            )

            self.session.add(user_settings)
        else:
            user_settings.user_first_name = self.first_name_var.get()
            user_settings.user_last_name = self.last_name_var.get()
            user_settings.user_company_registration_number = self.company_registration_number_var.get()
            user_settings.user_street = self.street_var.get()
            user_settings.user_street_number = self.street_number_var.get()
            user_settings.user_city = self.city_var.get()
            user_settings.user_country = self.country_var.get()
            user_settings.user_registered_as = self.registered_as_var.get()
            user_settings.invoice_due_date = self.invoice_due_date_var.get()
            user_settings.rate_per_hour = self.rate_per_hour_var.get()
            user_settings.currency = self.currency_var.get()
            user_settings.vat = self.vat_var.get()

        try:
            self.session.commit()
            messagebox.showinfo('Success', 'User settings saved successfully!')
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save user settings: {e}')
            self.session.rollback()
        finally:
            self.grab_release()
            self.destroy()
