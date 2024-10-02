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
