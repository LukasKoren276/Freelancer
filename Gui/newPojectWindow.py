import tkinter as tk
from tkinter import messagebox, font
from sqlalchemy.orm import Session

from Gui.customerSelectionWindow import CustomerSelectionWindow
from models import Project, Customer


class NewProjectWindow(tk.Toplevel):
    width = 550
    height = 300

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('New Project')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.selected_customer_id = None

        self.fields = {
            'project_name': (tk.StringVar(), 'Project Name')
        }

        self.create_window_objects()

    def create_window_objects(self):
        label_customer = tk.Label(self, text='Customer')
        label_customer.grid(row=0, column=0, padx=5, pady=20, sticky='S')
        self.customer_label = tk.Label(self, text="No customer selected")
        self.customer_label.grid(row=0, column=1, padx=5, pady=5)
        select_customer_button = tk.Button(self, text="Select Customer", command=self.open_customer_list_window)
        select_customer_button.grid(row=0, column=3, padx=5, pady=20, sticky='S')
        label_project_name = tk.Label(self, text="Project Name")
        label_project_name.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        entry_project_name = tk.Entry(self, textvariable=self.fields['project_name'][0], width=50)
        entry_project_name.grid(row=1, column=1, padx=5, pady=5)
        submit_button = tk.Button(self, text="Save and Close", command=self.submit)
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def open_customer_list_window(self):
        self.customer_list_window = CustomerSelectionWindow(self, self.session, self.set_selected_customer)

    def set_selected_customer(self, customer: Customer):
        self.selected_customer_id = customer.customer_id
        self.customer_label.config(
            text=f'{customer.company_name}' if customer.company_name else f'{customer.first_name} {customer.last_name}',
            font=font.Font(family="Helvetica", size=10, weight="bold"))                                                     # TODO move fonts to a separate class Fonts

    def submit(self):
        project_name = self.fields['project_name'][0].get()

        if not project_name:
            messagebox.showwarning("Validation Error", "Project Name cannot be empty.")
            return

        if not self.selected_customer_id:
            messagebox.showwarning("Validation Error", "Please select a customer for the project.")
            return

        new_project = Project(
            project_name=project_name,
            customer_id=self.selected_customer_id
        )

        self.session.add(new_project)

        try:
            self.session.commit()
            messagebox.showinfo('Success', 'Project saved successfully!')
        except Exception as e:
            messagebox.showinfo('Error', f'Failed to save the project: {e}')
            self.session.rollback()
        finally:
            self.grab_release()
            self.destroy()
