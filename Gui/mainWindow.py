from math import floor
import tkinter as tk
from sqlalchemy.orm import Session

from .editCustomersWindow import EditCustomersWindow
from .newCustomerWindow import NewCustomerWindow
from .settingsWindow import SettingsWindow


class MainWindow(tk.Tk):
    width = 800
    height = 600

    def __init__(self, title: str, session: Session):
        super().__init__()
        self.title(title)
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.label = tk.Label(self, text='Welcome to the Invoicer Application!')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.center_window()

        self.button_definitions = {
            'New Customer': self.new_customer,
            'Edit Customer': self.edit_customer,
            'New Project': self.new_project,
            'Edit Project': self.edit_project,
            'Log Project Time': self.log_time,
            'Edit Project Times': self.edit_log_time,
            'Create Offer': self.create_offer,
            'Create Invoice': self.create_invoice,
            'Settings': self.settings,
        }

        self.create_window_objects()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int(screen_width / 2 - self.width / 2)
        position_down = int(screen_height / 2 - self.height / 2)
        self.geometry(f"{self.width}x{self.height}+{position_right}+{position_down}")

    def create_window_objects(self):
        for index, (button_name, action) in enumerate(self.button_definitions.items()):
            button = tk.Button(self, text=button_name, command=action, width=15, height=2)
            button.grid(row=floor((index + 2)/2), column=index % 2, padx=10, pady=10)

    def new_customer(self):
        new_customer_window = NewCustomerWindow(self, self.session)
        new_customer_window.grab_set()

    def edit_customer(self):
        edit_customers_window = EditCustomersWindow(self, self.session)
        edit_customers_window.grab_set()

    def new_project(self):
        pass

    def edit_project(self):
        pass

    def log_time(self):
        pass

    def edit_log_time(self):
        pass

    def create_offer(self):
        pass

    def create_invoice(self):
        pass

    def settings(self):
        settings_window = SettingsWindow(self, self.session)
        settings_window.grab_set()


# def show(self):
    #     if self.window is None:
    #         self.create_window()
    #     self.window.deiconify()
    #
    # def hide(self):
    #     self.window.withdraw()
    #
    # def destroy(self):
    #     self.window.destroy()
