from helpers.constants import Constants


class WindowDetails:
    def __init__(self, title: str, width: int, height: int, resize: bool):
        self.title = title
        self.width = width
        self.height = height
        self.resize = resize

    @property
    def geometry(self):
        return f'{self.width}x{self.height}'

    @property
    def resizable(self):
        return self.resize, self.resize

    def get_title(self, entity_name: str,  operation: str) -> str:
        if operation == Constants.op_add:
            prefix = 'New'
        elif operation == Constants.op_edit:
            prefix = 'Edit'
        elif operation == Constants.op_delete:
            prefix = 'Delete'
        else:
            raise ValueError('Unknown operation for the title creation.')

        return f'{prefix} {entity_name}'

    def price_units(self) -> dict:
        return {
            'piece': 'pcs',
            'hour': 'hrs',
            'kilometer': 'km'
        }
