import customtkinter as ctk
from datetime import datetime
import calendar


# used from https://github.com/maxverwiebe/CTkDatePicker
class CTkDatePicker(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, width=20,  **kwargs)
        self.date_entry = ctk.CTkEntry(self, width=90)
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.calendar_button = ctk.CTkButton(self, text="▼", width=20, command=self.open_calendar)
        self.calendar_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.popup = None
        self.selected_date = None
        self.date_format = "%m/%d/%Y"
        self.allow_manual_input = True

    def set_date_format(self, date_format):
        self.date_format = date_format

    def open_calendar(self):
        if self.popup is not None:
            self.popup.destroy()
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Select Date")
        self.popup.geometry("+%d+%d" % (self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()))
        self.popup.resizable(False, False)
        self.popup.after(100, lambda: self.popup.focus())
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.build_calendar()

    def build_calendar(self):
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.destroy()

        self.calendar_frame = ctk.CTkFrame(self.popup)
        self.calendar_frame.grid(row=0, column=0)
        month_label = ctk.CTkLabel(
            self.calendar_frame,
            text=f"{calendar.month_name[self.current_month]}, {self.current_year}"
        )
        month_label.grid(row=0, column=1, columnspan=5)

        prev_month_button = ctk.CTkButton(self.calendar_frame, text="<", width=5, command=self.prev_month)
        prev_month_button.grid(row=0, column=0)

        next_month_button = ctk.CTkButton(self.calendar_frame, text=">", width=5, command=self.next_month)
        next_month_button.grid(row=0, column=6)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = ctk.CTkLabel(self.calendar_frame, text=day)
            lbl.grid(row=1, column=i)

        month_days = calendar.monthrange(self.current_year, self.current_month)[1]
        start_day = calendar.monthrange(self.current_year, self.current_month)[0]
        day = 1
        for week in range(2, 8):
            for day_col in range(7):
                if week == 2 and day_col < start_day:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                elif day > month_days:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                else:
                    btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=3,
                                        command=lambda day=day: self.select_date(day), fg_color="transparent")
                    btn.grid(row=week, column=day_col)
                    day += 1

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def select_date(self, day):
        self.selected_date = datetime(self.current_year, self.current_month, day)
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, ctk.END)
        self.date_entry.insert(0, self.selected_date.strftime(self.date_format))

        if not self.allow_manual_input:
            self.date_entry.configure(state='disabled')
        self.popup.destroy()
        self.popup = None

    def get_date(self):
        return self.date_entry.get()

    def set_allow_manual_input(self, value):
        self.allow_manual_input = value
        if not value:
            self.date_entry.configure(state='disabled')
        else:
            self.date_entry.configure(state='normal')
