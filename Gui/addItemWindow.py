import tkinter as tk

from .windowDetails import WindowDetails


class AddItemWindow(tk.Toplevel):
    width = 400
    height = 300

    def __init__(self, parent: tk.Tk, controller, window_details: WindowDetails):
        super().__init__(parent)
        self.controller = controller
        self.title(window_details.title)
        self.geometry(window_details.geometry)
        self.resizable(*window_details.resizable)
        self.item_type = tk.IntVar(value=1)
        self.create_window_objects()

    def create_window_objects(self):
        radio_project_specific = tk.Radiobutton(self, text="Project-specific item", variable=self.item_type, value=1)
        radio_project_specific.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        radio_common_item = tk.Radiobutton(self, text="Common item", variable=self.item_type, value=2)
        radio_common_item.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        create_button = tk.Button(self, text="Create Item", command=self.create_item)
        create_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def create_item(self):
        if self.item_type.get() == 1:
            self.controller.add_specific_item()
        else:
            self.controller.open_item_details_window()

        self.grab_release()
        self.destroy()
