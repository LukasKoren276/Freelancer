import customtkinter as ctk

from Gui.setup.windowDetails import WindowDetails


class MainWindow(ctk.CTk):

    def __init__(self, controller, window_details: WindowDetails):
        super().__init__()
        self.controller = controller
        self.window_details = window_details
        self.title(self.window_details.title)
        self.resizable(*self.window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, minsize=20)

        self.center_window()

        self.button_definitions = {
            'New Customer': self.controller.new_customer,
            'Edit Customer': self.controller.edit_customer,
            'New Project': self.controller.new_project,
            'Edit Project': self.controller.edit_project,
            'New Item': self.controller.new_item,
            'Edit Item': self.controller.edit_item,
            'Log Time': self.controller.log_time,
            'Create Offer': self.controller.create_offer,
            'Create Invoice': self.controller.create_invoice,
            'Settings': self.controller.open_settings
        }

        self.create_window_objects()

    def center_window(self) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int(screen_width / 2 - self.window_details.width / 2)
        position_down = int(screen_height / 2 - self.window_details.height / 2)
        self.geometry(f"{self.window_details.width}x{self.window_details.height}+{position_right}+{position_down}")

    def create_window_objects(self) -> None:
        button_font = ctk.CTkFont(family="Helvetica", size=15)

        for index, (button_name, action) in enumerate(self.button_definitions.items()):
            row = (index // 2) + 1
            column = (index % 2) + 1
            ctk.CTkButton(
                self, text=button_name, font=button_font, command=action
            ).grid(row=row, column=column, padx=30, pady=20, sticky='ew')
