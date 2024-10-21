import customtkinter as ctk


class IntSpinbox(ctk.CTkFrame):
    def __init__(
            self,
            parent,
            step: int = 1,
            width: int = 100,
            height: int = 32,
            low: int | None = None,
            hi: int | None = None
    ):
        super().__init__(parent, width=width, height=height)
        self.step = step
        self.low = low
        self.hi = hi
        self.configure(fg_color=("gray78", "gray28"))
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6, command=self.subtract)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6, command=self.add)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.entry.insert(0, '0')

    def add(self):
        input_value = self.entry.get()
        value = self.calculate_value(input_value, 'add')
        self.set_value(value)

    def subtract(self):
        input_value = self.entry.get()
        value = self.calculate_value(input_value, 'subtract')
        self.set_value(value)

    def get(self) -> float | None:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def calculate_value(self, input_value: str, calculation_type: str) -> int:
        try:
            if calculation_type == 'add':
                return int(input_value) + self.step if int(input_value) < self.hi else self.low
            if calculation_type == 'subtract':
                return int(input_value) - self.step if int(input_value) > self.low else self.hi
        except ValueError:
            return 0

    def set_value(self, value: int) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))

    def get_value(self):
        return self.entry.get()
