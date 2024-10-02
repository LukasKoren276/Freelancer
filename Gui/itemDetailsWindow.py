import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import Session
from models import Item, Price


class ItemDetailsWindow(tk.Toplevel):
    width = 400
    height = 300
    def __init__(self, parent: tk.Toplevel, session: Session, selected_project=None, item=None):
        super().__init__(parent)
        self.title('Item Details')
        self.session = session
        self.selected_project = selected_project  # Project-specific or None for common items
        self.item = item  # Existing item if editing, None if creating a new one
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)

        # Variables to store item details
        self.item_name_var = tk.StringVar(value=self.item.item_name if self.item else '')
        self.item_note_var = tk.StringVar(value=self.item.item_note if self.item else '')
        self.price_var = tk.StringVar(value=str(self.get_item_price()) if self.item else '')

        self.create_window_objects()

    def create_window_objects(self):
        # Entry fields for item details
        tk.Label(self, text="Item Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.item_name_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Item Note").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.item_note_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Price").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.price_var).grid(row=2, column=1, padx=10, pady=10)

        # Save button
        tk.Button(self, text="Save and Close", command=self.save_item).grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def get_item_price(self):
        """Retrieve the price of the item if it's an existing item."""
        if self.item:
            # Assuming there is a one-to-one relationship between item and price
            price = self.session.query(Price).filter_by(item_id=self.item.id).first()
            return price.price if price else 0
        return 0

    def save_item(self):
        # Validate the item details
        item_name = self.item_name_var.get().strip()
        item_note = self.item_note_var.get().strip()
        price = self.price_var.get().strip()

        if not item_name or not price:
            messagebox.showwarning("Validation Error", "Item name and price are required.")
            return

        try:
            # Convert price to a valid float
            price_value = float(price)
        except ValueError:
            messagebox.showwarning("Validation Error", "Invalid price format.")
            return

        if self.item:
            # Edit the existing item
            self.item.item_name = item_name
            self.item.item_note = item_note
            # Update the price
            item_price = self.session.query(Price).filter_by(item_id=self.item.id).first()
            if item_price:
                item_price.price = price_value
        else:
            # Create a new item
            new_item = Item(
                project_id=self.selected_project.id if self.selected_project else None,  # Use project ID for project-specific items
                item_name=item_name,
                item_note=item_note
            )
            self.session.add(new_item)
            self.session.flush()  # Flush to get the new item's ID

            # Create a new price entry for the item
            new_price = Price(
                item_id=new_item.id,
                price=price_value
            )
            self.session.add(new_price)

        try:
            # Commit the changes to the database
            self.session.commit()
            messagebox.showinfo("Success", "Item saved successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save item: {e}")
            self.session.rollback()
