import customtkinter as ctk
import ctypes
import sys

from helpers.constants import Constants


class WindowHelper:

    @staticmethod
    def get_title(entity_name: str, mode: str) -> str:
        match mode:
            case Constants.mode_add: prefix = 'New'
            case Constants.mode_edit: prefix = 'Edit'
            case Constants.mode_delete: prefix = 'Delete'
            case _: raise ValueError('Unknown operation for the title creation.')

        return f'{prefix} {entity_name}'

    @staticmethod
    def size_and_center(
            window: ctk.CTk | ctk.CTkToplevel,
            resiz: bool,
            center: bool = False,
            margin_ratio: float = 0.03
    ) -> None:
        window.update_idletasks()
        factor = WindowHelper.__get_dpi_scaling_factor()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = int(window.winfo_reqwidth() / factor) + int(screen_width * margin_ratio / factor)
        window_height = int(window.winfo_reqheight() / factor) + int(screen_height * margin_ratio / factor)

        if not center:
            window.geometry(f"{window_width}x{window_height}")
        else:
            WindowHelper.__center_window(window, window_width, window_height)

        window.resizable(resiz, resiz)

    @staticmethod
    def __get_dpi_scaling_factor() -> float:
        if sys.platform == "win32":
            hdc = ctypes.windll.user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            ctypes.windll.user32.ReleaseDC(0, hdc)

            return dpi / 96.0

        return 1.0

    @staticmethod
    def __center_window(window: ctk.CTkToplevel, window_width: int, window_height: int) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    @staticmethod
    def reset_combobox(combobox, values=None):
        if combobox:
            combobox.set('')
            combobox.configure(state='readonly' if values else 'disabled', values=values or [])
