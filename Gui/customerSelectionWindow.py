from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models import Customer


class CustomerSelectionWindow(tk.Toplevel):
    width = 1400
    height = 600

    def __init__(self, parent, session: Session, on_customer_selected):
        super().__init__(parent)
        self.session = session
        self.on_customer_selected = on_customer_selected
        self.title('Select Customer')
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(True, True)
        
        self.columns = {
            'company_name': 'Company Name',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'street': 'Street',
            'street_number': 'Street Number',
            'city': 'City',
            'country': 'Country',
            'company_registration_number': 'Company Registration Number'
        }
        
        self.create_customer_list()

    def create_customer_list(self):
        self.list_frame = tk.Frame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10)

        self.customer_list = ttk.Treeview(
            self.list_frame,
            columns=([key for key in self.columns.keys()]),
            show='headings',
            height=15
        )

        [self.customer_list.heading(key, text=value) for key, value in self.columns.items()]
        [self.customer_list.column(col, width=100, anchor=tk.W) for col in self.customer_list['columns']]
        self.customer_list.grid(row=0, column=0)

        scrollbar_y = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.customer_list.yview)
        self.customer_list.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.customer_list.bind('<Double-1>', self.select_customer)
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

    def select_customer(self, event=None):
        selected_item = self.customer_list.focus()

        if not selected_item:
            messagebox.showwarning('Select Customer', 'Please select a customer.')
            return

        selected_values = self.customer_list.item(selected_item, 'values')

        selected_customer = self.session.query(Customer).filter(
            Customer.first_name == selected_values[1],
            Customer.last_name == selected_values[2],
            or_(Customer.company_name == selected_values[0], Customer.company_name.is_(None))
        ).first()

        if not selected_customer:
            messagebox.showerror('Error', 'Customer not found.')
            return

        self.on_customer_selected(selected_customer)
        self.grab_release()
        self.destroy()
