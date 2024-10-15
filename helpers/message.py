import re
from CTkMessagebox import CTkMessagebox

from helpers.constants import Constants as Const


class Message:
    @staticmethod
    def show_msgbox(**kwargs) -> CTkMessagebox:
        return CTkMessagebox(
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
    def __prepare_db_message(result: bool, entity_name: str, mode: str) -> dict:
        title = 'Success' if result else 'Error'
        action = 'save' if mode == Const.mode_add else 'update' if mode == Const.mode_edit else Const.mode_delete

        message = (
            f'Failed to {action} {entity_name}.'
            if not result
            else f'{entity_name} was {action}d successfully. '
        )

        icon = 'check' if result else 'cancel'

        return {'title': title, 'message': message, 'icon': icon, 'option_1': 'OK'}

    @staticmethod
    def show_db_result(result: bool, entity_name: str, mode: str):
        Message.show_msgbox(**Message.__prepare_db_message(result, entity_name, mode))

    @staticmethod
    def common_one_button_msg(kind, title, message):
        if kind not in ['pass', 'fail']:
            raise ValueError("Kind has to be 'pass' or 'fail")

        icons = {
            'pass': 'check',
            'fail': 'cancel'
        }

        return Message.show_msgbox(**{'title': title, 'message': message, 'icon': icons.get(kind), 'option_1': 'OK'})




