from CTkMessagebox import CTkMessagebox
from sqlalchemy import inspect, Integer, String, DateTime
from datetime import datetime


class DataValidation:
    date_formats = [
        "%d.%m.%Y",
        "%d. %m. %Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]

    @staticmethod
    def validate_integer(value: str, is_nullable: bool) -> int | None:
        if value.strip() == '' and is_nullable:
            return None

        if value.strip().lstrip('-').isdigit():
            int_value = int(value)

            if int_value > 0:
                return int_value

            if int_value == 0:
                return None if is_nullable else 0

        return 0

    @staticmethod
    def validate_string(value: str, is_nullable: bool) -> str:
        if value.strip() != '':
            return value.strip()
        else:
            return None if is_nullable else ''

    @staticmethod
    def validate_datetime(value: str, is_nullable: bool) -> datetime | str:
        if value.strip() == '':
            return None if is_nullable else ''

        for fmt in DataValidation.date_formats:
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                continue

        return ''

    @staticmethod
    def validate_data(model, fields: dict) -> dict | None:
        columns = inspect(model).c
        validated_fields = {}

        for field_name, (var, _) in fields.items():
            value = var.get()
            column = columns[field_name]
            is_nullable = column.nullable

            if isinstance(column.type, Integer):
                new_value = DataValidation.validate_integer(value, is_nullable)

                if new_value == 0:
                    CTkMessagebox(
                        title='Invalid Input',
                        message=f'{field_name.replace("_", " ").title()} must be a valid positive integer.',
                        icon="cancel",
                        option_1='OK'
                    )
                    return

            elif isinstance(column.type, String):
                new_value = DataValidation.validate_string(value, is_nullable)
                if new_value == '':
                    CTkMessagebox(
                        title='Invalid Input',
                        message=f'{field_name.replace("_", " ").title()} must be a non-empty string.',
                        icon="cancel",
                        option_1='OK'
                    )
                    return

            elif isinstance(column.type, DateTime):
                new_value = DataValidation.validate_datetime(value, is_nullable)
                if new_value == '':
                    CTkMessagebox(
                        title='Invalid Input',
                        message=f'Date must be in one of the accepted formats: '
                                f'{", ".join(DataValidation.date_formats)}.',
                        icon="cancel",
                        option_1='OK'
                    )
                    return

            else:
                CTkMessagebox(
                    title='Invalid Data Format',
                    message='Data Format not recognized.',
                    icon="cancel",
                    option_1='OK'
                )
                return

            validated_fields[field_name] = new_value

        return validated_fields
