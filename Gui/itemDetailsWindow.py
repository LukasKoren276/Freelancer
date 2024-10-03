import tkinter as tk

from Gui.dataValidation import DataValidation
from Gui.windowDetails import WindowDetails
from models import Item, Price, Customer, Project


class ItemDetailsWindow(tk.Toplevel):

    def __init__(
            self,
            parent: tk.Tk,
            controller,
            window_details: WindowDetails,
            customer: Customer | None = None,
            project: Project | None = None,
            item: Item | None = None):
        super().__init__(parent)
        self.controller = controller
        self.customer = customer
        self.project = project
        self.item = item
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)

        self.item_fields = {
            'item_name': (tk.StringVar(value=self.item.item_name if self.item is not None else ''), 'Item Name'),
            'item_note': (tk.StringVar(value=self.item.item_note if self.item is not None else ''), 'Item Note')
        }

        self.price_fields = {
            'price': (tk.StringVar(
                value=str(self.controller.get_item_price(self.item.item_id))
                if self.item is not None
                else ''),
          'Item Price'),
        }

        self.create_window_objects()

    def create_window_objects(self):
        tk.Label(self, text='Customer').grid(row=0, column=0, padx=10, pady=10, sticky='W')
        tk.Label(self, text=self.get_customer_name()).grid(row=0, column=1, padx=10, pady=10, sticky='W')

        tk.Label(self, text='Project').grid(row=1, column=0, padx=10, pady=10, sticky='W')
        tk.Label(self, text=self.get_project_name()).grid(row=1, column=1, padx=10, pady=10, sticky='W')

        row = 2
        for name, (var, label_text) in {**self.item_fields, **self.price_fields}.items():
            tk.Label(self, text=label_text).grid(row=row, column=0, padx=10, pady=10, sticky='W')
            tk.Entry(self, textvariable=var).grid(row=row, column=1, padx=10, pady=10, sticky='W')
            row += 1

        tk.Button(self, text="Save and Close", command=self.save_item).grid(row=row + 1, column=0, columnspan=2, padx=10, pady=20)

    def get_customer_name(self) -> str:
        customer = None

        if self.customer is not None:
            customer = self.customer
        elif self.item is not None:
            customer = self.item.project.customer

        if customer is not None:
            return customer.company_name if customer.company_name else f'{customer.first_name} {customer.last_name}'

        return 'No customer for custom item'

    def get_project_name(self) -> str:
        project = None

        if self.project is not None:
            project = self.project
        elif self.item is not None:
            project = self.item.project

        if project is not None:
            return project.project_name

        return 'No project for custom item'

    def save_item(self):
        validated_item_data = DataValidation.validate_data(Item, self.item_fields)

        if validated_item_data is None:
            return

        if self.project is not None:
            validated_item_data.update({'project_id': self.project.project_id})

        validated_price_data = DataValidation.validate_data(Price, self.price_fields)

        if validated_price_data is None:
            return

        self.controller.save_item_with_price(validated_item_data, validated_price_data)
        self.grab_release()
        self.destroy()

        #
        # if self.item:
        #     # Edit the existing item
        #     self.item.item_name = item_name
        #     self.item.item_note = item_note
        #     # Update the price
        #     item_price = self.session.query(Price).filter_by(item_id=self.item.id).first()
        #     if item_price:
        #         item_price.price = price_value
        # else:
        #     # Create a new item
        #     new_item = Item(
        #         project_id=self.selected_project.id if self.selected_project else None,  # Use project ID for project-specific items
        #         item_name=item_name,
        #         item_note=item_note
        #     )
        #     self.session.add(new_item)
        #     self.session.flush()  # Flush to get the new item's ID
        #
        #     # Create a new price entry for the item
        #     new_price = Price(
        #         item_id=new_item.id,
        #         price=price_value
        #     )
        #     self.session.add(new_price)
        #
        # try:
        #     # Commit the changes to the database
        #     self.session.commit()
        #     messagebox.showinfo("Success", "Item saved successfully!")
        #     self.destroy()  # Close the window
        # except Exception as e:
        #     messagebox.showerror("Error", f"Failed to save item: {e}")
        #     self.session.rollback()
