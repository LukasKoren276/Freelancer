import customtkinter as ctk


class TimeMeasurementWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, time_management_window: ctk.CTkToplevel, text: str):
        super().__init__(parent)
        self.controller = controller
        self.time_management_window = time_management_window
        self.text = text

        self.setup_window()
        self.create_window_objects()

    def setup_window(self) -> None:
        self.title('Manage time for project items')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=50)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

    def create_window_objects(self):
        self.description_label = ctk.CTkLabel(self, text=self.text)
        self.description_label.grid(row=0, column=1, columnspan=5, padx=0, pady=(20, 0), sticky='SW')
