import customtkinter as ctk

from helpers.windowHelper import WindowHelper


class ModeSelectionWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, controller, title_name, names: tuple,  functions: tuple, modes: tuple):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.names = names
        self.functions = functions
        self.modes = modes
        self.title(f'{title_name} Management')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=80)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0, minsize=80)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1)
        self.grid_rowconfigure(0, minsize=20)
        self.__selected_function = None
        self.__selected_mode = None

        self.create_window_objects()

    def create_window_objects(self) -> None:
        row_index = 0
        for (name, function) in zip(self.names, self.functions):
            ctk.CTkLabel(
                self,
                text=f'Select operation type with {name}'
            ).grid(row=row_index, column=1, padx=0, pady=(20, 10), columnspan=3, sticky='w')
            row_index += 1

            for mode_index, mode in enumerate(self.modes):
                ctk.CTkButton(
                    self,
                    text=f'{mode.capitalize()} {name}',
                    command=lambda f=function, m=mode: self.__set_properties(f, m),
                    font=ctk.CTkFont(family="Helvetica", size=15)
                ).grid(row=row_index, column=2 * mode_index + 1, pady=(0, 20))

            row_index += 1

        WindowHelper.size_and_center(self, resiz=False, center=False, margin=20)

    def __set_properties(self, function, mode) -> None:
        self.__selected_function = function
        self.__selected_mode = mode
        self.destroy()

    def get_selected_function(self):
        return self.__selected_function

    def get_selected_mode(self):
        return self.__selected_mode
