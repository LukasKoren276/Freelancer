from math import floor
import tkinter as tk

from .windowDetails import WindowDetails


class MainWindow(tk.Tk):
    width = 800
    height = 600

    def __init__(self, controller, window_details: WindowDetails):
        super().__init__()
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.label = tk.Label(self, text='Welcome to the Invoicer Application!')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.center_window()

        self.button_definitions = {
            'New Customer': self.controller.new_customer,
            'Edit Customer': self.controller.edit_customer,
            'New Project': self.controller.new_project,
            'Edit Project': self.controller.edit_project,
            'Add Item': self.controller.add_item,
            'Edit Item': self.controller.edit_item,
            'Log Time': self.controller.log_time,
            'Create Offer': self.controller.create_offer,
            'Create Invoice': self.controller.create_invoice,
            'Settings': self.controller.open_settings
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
