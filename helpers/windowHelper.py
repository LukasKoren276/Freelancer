import customtkinter as ctk

from helpers.constants import Constants


class WindowHelper:

    @staticmethod
    def get_title(entity_name: str, mode: str) -> str:
        # TODO use match mode:
        if mode == Constants.mode_add:
            prefix = 'New'
        elif mode == Constants.mode_edit:
            prefix = 'Edit'
        elif mode == Constants.mode_delete:
            prefix = 'Delete'
        else:
            raise ValueError('Unknown operation for the title creation.')

        return f'{prefix} {entity_name}'

    @staticmethod
    def size_and_center(window: ctk.CTk | ctk.CTkToplevel, resiz: bool, center: bool = False, margin_ratio: float = 0.03) -> None:

        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_reqwidth() + int(screen_width * margin_ratio)
        window_height = window.winfo_reqheight() + int(screen_height * margin_ratio)

        if not center:
            window.geometry(f"{window_width}x{window_height}")
        else:
            WindowHelper.__center_window(window, window_width, window_height)

        window.resizable(resiz, resiz)

    @staticmethod
    def __center_window(window: ctk.CTkToplevel, window_width: int, window_height: int) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
