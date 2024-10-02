import tkinter as tk
from tkinter import messagebox, font

from Gui.dataValidation import DataValidation
from Gui.windowDetails import WindowDetails
from models import Project


class NewProjectWindow(tk.Toplevel):
    width = 550
    height = 300

    def __init__(self, parent,  controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.window_details = window_details
        self.title(self.window_details.title)
        self.geometry(self.window_details.geometry)
        self.resizable(*self.window_details.resizable)
        self.customer = None
        self.customer_label = None

        self.fields = {
            'project_name': (tk.StringVar(), 'Project Name')
        }

        self.create_window_objects()

    def create_window_objects(self):
        label_customer = tk.Label(self, text='Customer')
        label_customer.grid(row=0, column=0, padx=5, pady=20, sticky='S')
        self.customer_label = tk.Label(self, text="No customer selected")
        self.customer_label.grid(row=0, column=1, padx=5, pady=5)
        select_customer_button = tk.Button(self, text="Select Customer", command=self.set_selected_customer)
        select_customer_button.grid(row=0, column=3, padx=5, pady=20, sticky='S')
        label_project_name = tk.Label(self, text="Project Name")
        label_project_name.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        entry_project_name = tk.Entry(self, textvariable=self.fields['project_name'][0], width=50)
        entry_project_name.grid(row=1, column=1, padx=5, pady=5)
        submit_button = tk.Button(self, text="Save and Close", command=self.submit)
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def set_selected_customer(self):
        self.customer = self.controller.open_customer_selection(self)
        self.customer_label.config(
            text=f'{self.customer.company_name}'
            if self.customer.company_name
            else f'{self.customer.first_name} {self.customer.last_name}',
            font=font.Font(family="Helvetica", size=10, weight="bold")
        )
        # TODO move fonts to a separate class Fonts

    def submit(self):
        validated_data = DataValidation.validate_data(Project, self.fields)

        if not self.customer.customer_id:
            messagebox.showwarning('Invalid Input', 'Please select a customer for the project.')
            return

        if validated_data is None:
            return

        validated_data.update({'customer_id': self.customer.customer_id})
        self.controller.save_project(validated_data)
        self.grab_release()
        self.destroy()
