from tkinter import messagebox


class DataValidation:
    @staticmethod
    def integer(new_value):
        if new_value.isdigit():
            return True

        messagebox.showerror(
            'Invalid Input',
            'Please enter only numeric values.'
        )
        return False

    @staticmethod
    def integer_or_empty(new_value):
        if new_value == "" or new_value.isdigit():
            return True

        messagebox.showerror(
            'Invalid Input',
            'Please enter only numeric values or keep the field empty.'
        )
        return False
