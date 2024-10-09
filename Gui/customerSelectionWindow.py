import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from Gui.setup.windowDetails import WindowDetails


class CustomerSelectionWindow(ctk.CTkToplevel):

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
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_customer_list()

    def create_customer_list(self) -> None:
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.customer_list = ttk.Treeview(
            self.list_frame,
            columns=([key for key in self.columns.keys()]),
            show='headings'
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 13, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10),)

        for key, value in self.columns.items():
            self.customer_list.heading(key, text=value, anchor=tk.W)
            self.customer_list.column(key, anchor=tk.W)

        self.customer_list.grid(row=0, column=0, sticky='nsew')
        scrollbar_x = ttk.Scrollbar(self.list_frame, orient=tk.HORIZONTAL, command=self.customer_list.xview)
        scrollbar_y = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.customer_list.yview)
        self.customer_list.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        self.customer_list.bind('<Double-1>', self.select_customer_on_double_click)

        ctk.CTkButton(
            self,
            text='Select a Customer',
            font=ctk.CTkFont(family="Helvetica", size=15),
            command=self.select_customer_on_double_click
        ).grid(row=1, column=0, padx=10, pady=10)

        self.load_customers()
        self.autosize_columns()

    def autosize_columns(self) -> None:
        for col in self.customer_list['columns']:
            self.customer_list.column(col, width=ctk.CTkFont().measure(self.customer_list.heading(col)['text']))
            for row in self.customer_list.get_children(''):
                item_width = ctk.CTkFont().measure(self.customer_list.set(row, col))
                self.customer_list.column(col, width=max(self.customer_list.column(col, 'width'), item_width))

    def load_customers(self) -> None:
        for i in self.customer_list.get_children():
            self.customer_list.delete(i)

        customers = self.controller.get_customers()

        for index, customer in enumerate(customers):
            item_id = self.customer_list.insert(
                '',
                'end',
                values=(
                    customer.company_name if customer.company_name is not None else '',
                    customer.first_name,
                    customer.last_name,
                    customer.street,
                    customer.street_number,
                    customer.city,
                    customer.country,
                    customer.company_registration_number
                )
            )

            if index % 2 == 0:
                self.customer_list.item(item_id, tags=('evenrow',))

        self.customer_list.tag_configure('evenrow', background='#d3d3d3')

    def select_customer_on_double_click(self, event=None) -> None:
        selected_item = self.customer_list.focus()

        if not selected_item:
            CTkMessagebox(
                title='Select Customer',
                message='Please select a customer.',
                icon="cancel",
                option_1='OK'
            ).get()

            self.grab_set()
        else:
            self.customer_values = self.customer_list.item(selected_item, 'values')
            self.destroy()

    def get_customer_values(self) -> tuple:
        return self.customer_values
