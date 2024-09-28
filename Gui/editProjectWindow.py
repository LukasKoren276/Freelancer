import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session

from models import Project
from .customerSelectionWindow import CustomerSelectionWindow
from .editProjectNameWindow import EditProjectNameWindow


class EditProjectWindow(tk.Toplevel):
    width = 450
    height = 250

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('Edit Project')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.selected_customer_id = None
        self.selected_project = None
        self.create_window_objects()

    def create_window_objects(self):
        self.customer_button = tk.Button(self, text="Select Customer", command=self.open_customer_selection)
        self.customer_button.grid(row=0, column=0, padx=10, pady=40, sticky='S')
        self.customer_label = tk.Label(self, text="No customer selected")
        self.customer_label.grid(row=0, column=1, padx=10, pady=40, sticky='S')
        self.project_label = tk.Label(self, text="Select Project")
        self.project_label.grid(row=2, column=0, padx=10, pady=10)
        self.project_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.project_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.edit_project_button = tk.Button(self, text="Edit Project", command=self.open_edit_project_window)
        self.edit_project_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def open_customer_selection(self):
        customer_selection_window = CustomerSelectionWindow(self, self.session, self.set_selected_customer)
        customer_selection_window.grab_set()

    def set_selected_customer(self, selected_customer):
        self.selected_customer_id = selected_customer.customer_id

        self.customer_label.config(
            text=f'{selected_customer.company_name}'
            if selected_customer.company_name
            else f'{selected_customer.first_name} {selected_customer.last_name}'
        )

        self.load_customer_projects()

    def load_customer_projects(self):
        projects = self.session.query(Project).filter_by(customer_id=self.selected_customer_id).all()
        project_names = [project.project_name for project in projects]
        self.project_combobox['values'] = project_names
        if project_names:
            self.project_combobox.current(0)  # Set the first project as the default

    def open_edit_project_window(self):
        selected_project_name = self.project_combobox.get()
        if not selected_project_name:
            messagebox.showwarning("Select Project", "Please select a project to edit.")
            return

        self.selected_project = self.session.query(Project).filter_by(
            project_name=selected_project_name, customer_id=self.selected_customer_id
        ).first()

        if self.selected_project:
            edit_project_name_window = EditProjectNameWindow(
                self,
                self.session,
                self.selected_project,
                self.refresh_project_list
            )

            edit_project_name_window.grab_set()

    def refresh_project_list(self):
        self.load_customer_projects()
