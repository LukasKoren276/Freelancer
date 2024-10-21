import customtkinter as ctk

from helpers.windowHelper import WindowHelper


class MainWindow(ctk.CTk):

    def __init__(self, window_title, controller):
        super().__init__()
        self.title(window_title)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=80)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0, minsize=80)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1)
        self.grid_rowconfigure(0, minsize=20)

        self.button_definitions = {
            'Customer management': self.controller.customer_management,
            'Project Management': self.controller.project_management,
            'Item management': self.controller.item_management,
            'Item Time management': self.controller.time_management,
            'Create Offer': self.controller.create_offer,
            'Create Invoice': self.controller.create_invoice,
            'Settings': self.controller.settings_window
        }

        self.create_window_objects()

    def create_window_objects(self) -> None:
        button_font = ctk.CTkFont(family="Helvetica", size=15)

        for index, (button_name, action) in enumerate(self.button_definitions.items()):
            row = (index // 3) * 3
            column = 1 if index % 3 == 0 else 3 if index % 3 == 1 else 5

            ctk.CTkButton(
                self, text=button_name, font=button_font, command=action
            ).grid(row=row, column=column, padx=0, pady=(40, 0), sticky='ew')

        WindowHelper.size_and_center(self, resiz=False, center=True)
