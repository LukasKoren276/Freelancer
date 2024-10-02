import tkinter as tk
from tkinter import ttk, messagebox, font

from .windowDetails import WindowDetails


class EditProjectWindow(tk.Toplevel):
    width = 450
    height = 250

    def __init__(self, parent,  controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.window_details = window_details
        self.title(self.window_details.title)
        self.geometry(self.window_details.geometry)
        self.resizable(*self.window_details.resizable)
        self.customer_label = None
        self.project_combobox = None
        self.customer = None
        self.selected_project = None
        self.create_window_objects()

    def create_window_objects(self):
        customer_button = tk.Button(self, text="Select Customer", command=self.set_selected_customer)
        customer_button.grid(row=0, column=0, padx=10, pady=40, sticky='S')
        self.customer_label = tk.Label(self, text="No customer selected")
        self.customer_label.grid(row=0, column=1, padx=10, pady=40, sticky='S')
        project_label = tk.Label(self, text="Select Project")
        project_label.grid(row=2, column=0, padx=10, pady=10)
        self.project_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.project_combobox.grid(row=2, column=1, padx=10, pady=10)
        edit_project_button = tk.Button(self, text="Edit Project", command=self.open_edit_project_window)
        edit_project_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def set_selected_customer(self):
        self.customer = self.controller.open_customer_selection(self)

        self.customer_label.config(
            text=f'{self.customer.company_name}'
            if self.customer.company_name
            else f'{self.customer.first_name} {self.customer.last_name}',
            font=font.Font(family="Helvetica", size=10, weight="bold")
        )
        # TODO move fonts to a separate class Fonts

        self.load_customer_projects()

    def load_customer_projects(self):
        projects = self.controller.get_customer_projects(self.customer.customer_id)
        project_names = [project.project_name for project in projects]
        self.project_combobox['values'] = project_names
        if project_names:
            self.project_combobox.current(0)

    def open_edit_project_window(self):
        selected_project_name = self.project_combobox.get()

        if not selected_project_name:
            messagebox.showwarning("Select Project", "Please select a project to edit.")
            return

        self.selected_project = self.controller.get_project_by_customer_id_and_name(
            self.customer.customer_id,
            selected_project_name
        )

        if self.selected_project:
            self.controller.edit_project_name(self.customer, self.selected_project)
            self.refresh_project_list()
            self.grab_release()
            self.destroy()

    def refresh_project_list(self):
        self.load_customer_projects()
