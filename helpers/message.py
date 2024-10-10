import re

from CTkMessagebox import CTkMessagebox
from models import Base


class Message:
    @staticmethod
    def __show_msgbox(**kwargs):
        CTkMessagebox(
            title=kwargs.get('title'),
            message=kwargs.get('message'),
            icon=kwargs.get('icon'),
            option_1=kwargs.get('option_1'),
            option_2=kwargs.get('option_2'),
            option_3=kwargs.get('option_3')
        ).get()

    @staticmethod
    def __split_camel_case(string: str) -> str:
        return ' '.join(re.findall(r'[A-Z][a-z]*', string))

    @staticmethod
    def __prepare_db_message(result: bool, entity_name: str, instance: Base) -> dict:
        title = 'Success' if result else 'Error'
        action = 'save' if instance is None else 'update'

        message = (
            f'Failed to {action} {entity_name}.'
            if not result
            else f'{entity_name} was {action}d successfully. '
        )

        icon = 'check' if result else 'cancel'

        return {'title': title, 'message': message, 'icon': icon, 'option_1': 'OK'}

    @staticmethod
    def show_db_result(result: bool, entity_name: str, instance: Base):
        Message.__show_msgbox(**Message.__prepare_db_message(result, entity_name, instance))

    @staticmethod
    def common_one_button_msg(kind, title, message):
        if kind not in ['pass', 'fail']:
            raise ValueError("Kind has to be 'pass' or 'fail")

        icons = {
            'pass': 'check',
            'fail': 'cancel'
        }

        return Message.__show_msgbox(**{'title': title, 'message': message, 'icon': icons.get(kind), 'option_1': 'OK'})




