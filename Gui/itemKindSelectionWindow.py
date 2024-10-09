import customtkinter as ctk

from Gui.setup.windowDetails import WindowDetails


class ItemKindSelectionWindow(ctk.CTkToplevel):

    def __init__(self, parent, controller, window_details: WindowDetails, operation: str):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.operation = operation
        self.title('Select Item Operation')
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.selected_method = None

        self.create_window_objects()

    def create_window_objects(self) -> None:
        ctk.CTkLabel(
            self,
            text=f'What kind of item would you like to {self.operation}'
        ).grid(row=0, column=1, padx=0, pady=0)

        ctk.CTkButton(
            self,
            text=f'{self.operation.capitalize()} General Item',
            command=lambda: self.set_selected_method(self.controller.general_item),
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=1, column=1, sticky='W')

        ctk.CTkButton(
            self,
            text=f'{self.operation.capitalize()} Specific Item',
            command=lambda: self.set_selected_method(self.controller.specific_item),
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=1, column=2, sticky='E')

    def set_selected_method(self, method) -> None:
        self.selected_method = method
        self.destroy()

    def get_selected_method(self):
        return self.selected_method
