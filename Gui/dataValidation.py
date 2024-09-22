import tkinter as tk
from tkinter import messagebox
from sqlalchemy.inspection import inspect


class DataValidation:
    @staticmethod
    def positive_integer(value: int) -> bool:
        if isinstance(value, int) and value > 0:
            return True

        return False

    @staticmethod
    def non_empty_string(value: str) -> bool:
        if value.strip() == '':
            return False

        return True

    @staticmethod
    def is_data_valid(model, fields: dict) -> bool:
        columns = inspect(model).c

        for field_name, (var, _) in fields.items():
            value = var.get()
            is_nullable = columns[field_name].nullable

            if not is_nullable and isinstance(var, tk.IntVar):
                if not DataValidation.positive_integer(value):
                    messagebox.showwarning(
                        'Invalid Input',
                        f'{field_name.replace("_", " ").title()} must be a positive integer.')

                    return False

            if not is_nullable and isinstance(var, tk.StringVar):
                if not DataValidation.non_empty_string(value):
                    messagebox.showwarning(
                        'Invalid Input',
                        f'{field_name.replace("_", " ").title()} cannot be empty.'
                    )

                    return False

        return True

    @staticmethod
    def convert_empty_fields_to_null(data: dict) -> dict:
        for field_name in data.keys():
            if isinstance(data[field_name], int):
                data[field_name] = None if data[field_name] == 0 else data[field_name]

            if isinstance(data[field_name], str):
                data[field_name] = None if data[field_name] == '' else data[field_name]
        return data

