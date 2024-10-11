import customtkinter as ctk

from helpers.windowHelper import WindowHelper


class ItemKindSelectionWindow(ctk.CTkToplevel):

    def __init__(self, parent, title, controller, mode: str):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.mode = mode
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=50)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.selected_method = None

        self.create_window_objects()

    def create_window_objects(self) -> None:
        ctk.CTkLabel(
            self,
            text=f'What kind of item would you like to {self.mode}'
        ).grid(row=0, column=1, padx=0, pady=0, columnspan=3, sticky='w')

        ctk.CTkButton(
            self,
            text=f'{self.mode.capitalize()} General Item',
            command=lambda: self.set_selected_method(self.controller.__general_item_window),
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=1, column=1, sticky='e')

        ctk.CTkButton(
            self,
            text=f'{self.mode.capitalize()} Specific Item',
            command=lambda: self.set_selected_method(self.controller.__specific_item_window),
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=1, column=3, sticky='e')

        WindowHelper.size_and_center(self, resiz=False, center=False)

    def set_selected_method(self, method) -> None:
        self.selected_method = method
        self.destroy()

    def get_selected_method(self):
        return self.selected_method
