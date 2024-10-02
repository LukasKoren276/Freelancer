import tkinter as tk
from tkinter import messagebox, font

from Gui.dataValidation import DataValidation
from Gui.windowDetails import WindowDetails
from models import Project, Customer


class EditProjectNameWindow(tk.Toplevel):
    width = 370
    height = 150

    def __init__(self, parent, controller, window_details: WindowDetails, customer: Customer, project: Project):
        super().__init__(parent)
        self.controller = controller
        self.window_details = window_details
        self.customer = customer
        self.project = project
        self.title(self.window_details.title)
        self.geometry(self.window_details.geometry)
        self.resizable(*self.window_details.resizable)
        self.project_name_entry = None

        self.fields = {
            'project_name': (tk.StringVar(), 'Project Name')
        }

        self.create_window_objects()

    def create_window_objects(self):
        customer_label = tk.Label(self, text="Customer")
        customer_label.grid(row=0, column=0, padx=10, pady=10)

        customer_name_label = tk.Label(
            self,
            text=f'{self.customer.company_name}'
            if self.customer.company_name
            else f'{self.customer.first_name} {self.customer.last_name}',
            font=font.Font(family="Helvetica", size=10, weight="bold"))
        customer_name_label.grid(row=0, column=1, padx=10, pady=10)

        project_name_label = tk.Label(self, text="Project Name")
        project_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.project_name_entry = tk.Entry(self, textvariable=self.fields['project_name'][0], width=40)
        self.project_name_entry.grid(row=1, column=1, padx=10, pady=10)

        save_button = tk.Button(self, text="Save and Close", command=self.save_project_name)
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def save_project_name(self):
        new_project_name = self.project_name_entry.get()

        if not new_project_name.strip():
            messagebox.showwarning("Validation Error", "Project name cannot be empty.")
            return

        validated_data = DataValidation.validate_data(Project, self.fields)
        self.controller.update_project(self.project, validated_data)
        self.grab_release()
        self.destroy()
