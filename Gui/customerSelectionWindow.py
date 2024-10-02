import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Gui.windowDetails import WindowDetails


class CustomerSelectionWindow(tk.Toplevel):

    def __init__(self, parent, controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)

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

        self.list_frame = None
        self.customer_list = None
        self.customer_values = None
        self.selected_customer = None
        self.create_customer_list()

    def create_customer_list(self):
        self.list_frame = tk.Frame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10)

        self.customer_list = ttk.Treeview(
            self.list_frame,
            columns=([key for key in self.columns.keys()]),     # TODO make the column names bold
            show='headings',
            height=27                                           # TODO wider Treeview
        )

        [self.customer_list.heading(key, text=value) for key, value in self.columns.items()]
        [self.customer_list.column(col, width=100, anchor=tk.W) for col in self.customer_list['columns']]
        self.customer_list.grid(row=0, column=0)
        scrollbar_y = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.customer_list.yview)
        self.customer_list.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.customer_list.bind('<Double-1>', self.select_customer_on_double_click)
        select_button = tk.Button(self, text='Select', command=self.select_customer_on_double_click, width=15, height=2)
        select_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)  # Allow the Treeview to expand
        self.list_frame.grid_columnconfigure(0, weight=1)  # Allow the Treeview to expand
        self.load_customers()

    def load_customers(self):
        for i in self.customer_list.get_children():
            self.customer_list.delete(i)

        customers = self.controller.get_customers()

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

    def select_customer_on_double_click(self, event=None):
        selected_item = self.customer_list.focus()

        if not selected_item:
            messagebox.showwarning('Select Customer', 'Please select a customer.')
            return

        self.customer_values = self.customer_list.item(selected_item, 'values')
        self.destroy()

    def get_customer_values(self):
        return self.customer_values
