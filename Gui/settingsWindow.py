import tkinter as tk

from Gui.setup.windowDetails import WindowDetails
from models import UserSettings
from helpers.dataValidation import DataValidation


class SettingsWindow(tk.Toplevel):
    width = 500
    height = 550

    def __init__(self, parent, controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
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
        user_settings = self.controller.get_user_settings()

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
        user_settings = self.controller.get_user_settings()
        validated_data = DataValidation.validate_data(UserSettings, self.fields)

        if validated_data is None:
            return

        if not user_settings:
            self.controller.save_user_settings(validated_data)
        else:
            self.controller.update_user_settings(user_settings, validated_data)

        self.grab_release()
        self.destroy()
