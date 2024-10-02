import tkinter as tk
from sqlalchemy.orm import Session

from .editProjectWindow import EditProjectWindow  # Reuse EditProjectWindow
from .itemDetailsWindow import ItemDetailsWindow


class AddItemWindow(tk.Toplevel):
    width = 400
    height = 300

    def __init__(self, parent: tk.Tk, session: Session):
        super().__init__(parent)
        self.title('Add or Edit Item')
        self.session = session
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)

        self.item_type = tk.IntVar(value=1)  # 1 = Project-specific, 2 = Common

        self.create_window_objects()

    def create_window_objects(self):
        self.radio_project_specific = tk.Radiobutton(self, text="Project-specific item", variable=self.item_type, value=1)
        self.radio_common_item = tk.Radiobutton(self, text="Common item", variable=self.item_type, value=2)
        self.radio_project_specific.grid(row=0, column=0, padx=10, pady=10)
        self.radio_common_item.grid(row=1, column=0, padx=10, pady=10)

        self.create_button = tk.Button(self, text="Create Item", command=self.create_item)
        self.create_button.grid(row=2, column=0, padx=10, pady=10)

        self.edit_button = tk.Button(self, text="Edit Item", command=self.edit_item)
        self.edit_button.grid(row=3, column=0, padx=10, pady=10)

    def create_item(self):
        if self.item_type.get() == 1:  # Project-specific item
            edit_project_window = EditProjectWindow(self, self.session, self.open_item_details_window)
            edit_project_window.grab_set()
        else:  # Common item
            self.open_item_details_window(None)

    def edit_item(self):
        # Logic to fetch the existing item from the database (perhaps via a selection window)
        selected_item = ...  # Retrieve selected item from the database or list
        self.open_item_details_window(None, selected_item)

    def open_item_details_window(self, selected_project, selected_item=None):
        item_details_window = ItemDetailsWindow(self, self.session, selected_project, selected_item)
        item_details_window.grab_set()
