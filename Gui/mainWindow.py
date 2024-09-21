
import tkinter as tk
from sqlalchemy.orm import Session

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
        self.create_window_objects()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int(screen_width / 2 - self.width / 2)
        position_down = int(screen_height / 2 - self.height / 2)
        self.geometry(f"{self.width}x{self.height}+{position_right}+{position_down}")

    def create_window_objects(self):
        settings_button = tk.Button(self, text='Settings', command=self.open_settings, width=15, height=2)
        settings_button.grid(row=1, column=0, padx=10, pady=10)

        new_customer_button = tk.Button(self, text='New Customer', command=self.open_new_customer, width=15, height=2)
        new_customer_button.grid(row=2, column=0, padx=10, pady=10)

        edit_customer_button = tk.Button(self, text='Edit Customer', command=self.open_edit_customer, width=15, height=2)
        edit_customer_button.grid(row=2, column=1, padx=10, pady=10)

        new_project_button = tk.Button(self, text='New Project', command=self.open_new_project, width=15, height=2)
        new_project_button.grid(row=3, column=0, padx=10, pady=10)

        edit_project_button = tk.Button(self, text='Edit Project', command=self.open_edit_project, width=15, height=2)
        edit_project_button.grid(row=3, column=1, padx=10, pady=10)

        time_log = tk.Button(self, text='Log Project Time', command=self.open_log_time, width=15, height=2)
        time_log.grid(row=4, column=0, padx=10, pady=10)

        time_log_edit = tk.Button(self, text='Edit Project Times', command=self.edit_log_time, width=15, height=2)
        time_log_edit.grid(row=4, column=1, padx=10, pady=10)

        create_invoice = tk.Button(self, text='Create Invoice', command=self.make_invoice, width=15, height=2)
        create_invoice.grid(row=5, column=0, padx=10, pady=10)

    def open_settings(self):
        settings_window = SettingsWindow(self, self.session)
        settings_window.grab_set()

    def open_new_customer(self):
        new_customer_window = NewCustomerWindow(self, self.session)
        new_customer_window.grab_set()

    def open_edit_customer(self):
        pass

    def open_new_project(self):
        pass

    def open_edit_project(self):
        pass

    def open_log_time(self):
        pass

    def edit_log_time(self):
        pass

    def make_invoice(self):
        pass

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
