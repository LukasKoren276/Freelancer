import customtkinter as ctk

from helpers.windowHelper import WindowHelper


class MainWindow(ctk.CTk):

    def __init__(self, window_title, controller):
        super().__init__()
        self.title(window_title)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, minsize=20)

        self.button_definitions = {
            'New Customer': self.controller.new_customer_window,
            'Edit Customer': self.controller.edit_customer_window,
            'New Project': self.controller.new_project_window,
            'Edit Project': self.controller.edit_project_window,
            'New Item': self.controller.new_item_window,
            'Edit Item': self.controller.edit_item_window,
            'Log Time': self.controller.log_time,
            'Create Offer': self.controller.create_offer,
            'Create Invoice': self.controller.create_invoice,
            'Settings': self.controller.settings_window
        }

        self.create_window_objects()

    def create_window_objects(self) -> None:
        button_font = ctk.CTkFont(family="Helvetica", size=15)

        for index, (button_name, action) in enumerate(self.button_definitions.items()):
            row = (index // 2) + 1
            column = (index % 2) + 1
            ctk.CTkButton(
                self, text=button_name, font=button_font, command=action
            ).grid(row=row, column=column, padx=30, pady=20, sticky='ew')

        WindowHelper.size_and_center(self, resiz=False, center=True)
