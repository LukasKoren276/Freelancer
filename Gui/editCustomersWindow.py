import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy.orm import Session

from Gui.editCustomerWindow import EditCustomerWindow
from models import Customer


class EditCustomersWindow(tk.Toplevel):
    width = 1400
    height = 600

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('Edit Customer')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(True, True)
        self.selected_customer = None
        self.create_customer_list()
        self.edit_button = tk.Button(self, text="Edit", command=self.open_edit_window)
        self.edit_button.pack(pady=20)

    def create_customer_list(self):
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.customer_list = ttk.Treeview(
            self.list_frame,
            columns=("company_name",
                     "first_name",
                     "last_name",
                     "street",
                     "street_number",
                     "city",
                     "country",
                     "company_registration_number"
                     ),
            show='headings')

        self.customer_list.heading("company_name", text="Company Name")
        self.customer_list.heading("first_name", text="First Name")
        self.customer_list.heading("last_name", text="Last Name")
        self.customer_list.heading("street", text="Street")
        self.customer_list.heading("street_number", text="Street Number")
        self.customer_list.heading("city", text="City")
        self.customer_list.heading("country", text="Country")
        self.customer_list.heading("company_registration_number", text="Company Registration Number")

        for col in self.customer_list["columns"]:
            self.customer_list.column(col, width=100, anchor=tk.W)

        self.scrollbar_y = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.customer_list.yview)
        self.customer_list.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.customer_list.pack(fill=tk.BOTH, expand=True)
        self.customer_list.bind("<Double-1>", self.open_edit_window)
        self.load_customers()

    def load_customers(self):
        for i in self.customer_list.get_children():
            self.customer_list.delete(i)

        customers = self.session.query(Customer).all()

        for customer in customers:
            self.customer_list.insert(
                '',
                'end',
                values=(
                    customer.company_name,
                    customer.first_name,
                    customer.last_name,
                    customer.street,
                    customer.street_number,
                    customer.city,
                    customer.country,
                    customer.company_registration_number
                )
            )

    def open_edit_window(self, event=None):
        selected_item = self.customer_list.focus()

        if not selected_item:
            messagebox.showwarning("Select Customer", "Please select a customer to edit.")
            return

        selected_values = self.customer_list.item(selected_item, 'values')

        self.selected_customer = self.session.query(Customer).filter_by(
            first_name=selected_values[1],
            last_name=selected_values[2],
            company_name=selected_values[0]
        ).first()

        if not self.selected_customer:
            messagebox.showerror("Error", "Customer not found.")
            return

        self.edit_window = EditCustomerWindow(self, self.session, self.selected_customer)

    def refresh_list(self):
        self.load_customers()
