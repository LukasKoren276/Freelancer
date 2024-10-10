import customtkinter as ctk


from helpers.dataValidation import DataValidation
from helpers.windowHelper import WindowHelper
from models import UserSettings

class SettingsWindow(ctk.CTkToplevel):
    width = 500
    height = 550

    def __init__(self, parent, window_title, controller):
        super().__init__(parent)
        self.controller = controller
        self.title(window_title)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.fields = {
            'user_first_name': (ctk.StringVar(), 'First Name'),
            'user_last_name': (ctk.StringVar(), 'Last Name'),
            'user_street': (ctk.StringVar(), 'Street'),
            'user_street_number': (ctk.StringVar(), 'Street Number'),
            'user_city': (ctk.StringVar(), 'City'),
            'user_country': (ctk.StringVar(), 'Country'),
            'company_name': (ctk.StringVar(), 'Company Name'),
            'user_company_registration_number': (ctk.StringVar(), 'Company Registration Number'),
            'user_registered_as': (ctk.StringVar(), 'User Registered As'),
            'invoice_due_date': (ctk.StringVar(), 'Invoice Due Date [days]'),
            'rate_per_hour': (ctk.StringVar(), 'Rate Per Hour'),
            'currency': (ctk.StringVar(), 'Currency'),
            'vat': (ctk.StringVar(), 'VAT [%]')
        }

        self.load_user_settings()
        self.create_window_objects()

    def load_user_settings(self) -> None:
        user_settings = self.controller.get_user_settings()

        if user_settings:
            for field_name, (var, _) in self.fields.items():
                value = getattr(user_settings, field_name, None)

                if value is not None:
                    var.set(value)

    def create_window_objects(self) -> None:
        for index, (name, (var, label_text)) in enumerate(self.fields.items()):
            ctk.CTkLabel(
                self,
                text=label_text
            ).grid(row=2 * index, column=1, padx=0, pady=0 if index != 0 else (20, 0), sticky='SW')

            ctk.CTkEntry(
                self,
                textvariable=var,
                width=300
            ).grid(row=2 * index + 1, column=1, padx=0, pady=(0, 5), sticky='NW')

        ctk.CTkButton(
            self,
            text='Save and Close',
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=2 * len(self.fields) + 1, column=1, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False, center=False)

    def submit(self) -> None:
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
