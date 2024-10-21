import customtkinter as ctk
from tkinter import ttk
from datetime import datetime


from Gui.datePicker import CTkDatePicker
from Gui.intSpinbox import IntSpinbox
from helpers.constants import Constants as Const
from helpers.dateTimeHelper import DateTimeHelper
from helpers.message import Message
from helpers.windowHelper import WindowHelper


class TimeSpentWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, time_management_window: ctk.CTkToplevel, text: str):
        super().__init__(parent)
        self.controller = controller
        self.time_management_window = time_management_window
        self.text = text

        self.columns = {
            'record_date': 'Date',
            'duration_seconds': 'Duration',
            'item_time_note': 'Note'
        }

        self.setup_window()
        self.create_window_objects()

    def setup_window(self) -> None:
        self.title('Add Time for your Item')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0, minsize=80)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0, minsize=80)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1)

    def create_window_objects(self):
        row = 0

        ctk.CTkLabel(self, text=self.text).grid(row=row, column=1, columnspan=10, padx=0, pady=(20, 15), sticky='SEW')
        row += 1

        ctk.CTkLabel(
            self, text=f'Customer:\t{self.time_management_window.text_customer()}'
        ).grid(row=row, column=1, columnspan=10, padx=0, pady=0, sticky='SW')
        row += 1

        ctk.CTkLabel(
            self, text=f'Project:\t\t{self.time_management_window.selected_project.project_name}'
        ).grid(row=row, column=1, columnspan=10, padx=0, pady=0, sticky='SW')
        row += 1

        ctk.CTkLabel(
            self, text=f'Item:\t\t{self.time_management_window.selected_item.item_name}'
        ).grid(row=row, column=1, columnspan=10, padx=0, pady=(0, 30), sticky='SW')
        row += 1

        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=row, column=1, columnspan=5, padx=0, pady=0, sticky='nsew')
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_propagate(False)

        self.item_time_list = ttk.Treeview(
            self.list_frame,
            columns=([key for key in self.columns.keys()]),
            show='headings',
            height=5
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 13, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))

        for key, value in self.columns.items():
            self.item_time_list.heading(key, text=value, anchor=ctk.W)
            self.item_time_list.column(key, anchor=ctk.W)

        self.item_time_list.grid(row=0, column=0, sticky='nsew')
        scrollbar_y = ttk.Scrollbar(self.list_frame, orient=ctk.VERTICAL, command=self.item_time_list.yview)
        self.item_time_list.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        row += 1

        self.load_item_times()

        ctk.CTkLabel(
            self,
            text='Total Recorded Time for Item:\t' + DateTimeHelper.convert_seconds_to_time_string(
                self.time_management_window.item_duration_sum
            )
        ).grid(row=row, column=1, columnspan=10, padx=0, pady=(20, 30), sticky='SW')
        row += 1

        ctk.CTkLabel(self, text='Select date:').grid(row=row, column=1, padx=0, pady=0, sticky='EW')
        ctk.CTkLabel(self, text='Duration hours:').grid(row=row, column=3, padx=0, pady=0, sticky='SEW')
        ctk.CTkLabel(self, text='Duration minutes:').grid(row=row, column=5, padx=0, pady=0, sticky='SEW')
        row += 1

        self.date_picker = CTkDatePicker(self)
        self.date_picker.set_allow_manual_input(False)
        self.date_picker.grid(row=row, column=1, pady=(0, 15), sticky='SEW')

        self.hour_spin_box = IntSpinbox(self, low=0, hi=24)
        self.hour_spin_box.grid(row=row, column=3, padx=0, pady=(0, 15), sticky='SEW')

        self.minute_spin_box = IntSpinbox(self, low=0, hi=59)
        self.minute_spin_box.grid(row=row, column=5, padx=0, pady=(0, 15), sticky='SEW')
        row += 1

        ctk.CTkLabel(self, text='Record Note:').grid(row=row, column=1, padx=0, pady=(30, 30), sticky='SW')

        self.note_entry = ctk.CTkEntry(
            self,
            textvariable=ctk.StringVar(),
            width=310)
        self.note_entry.grid(row=row, column=2, padx=0, pady=(30, 30), sticky='SW', columnspan=10)
        row += 1

        button_add_spent_time = ctk.CTkButton(
            self,
            text='Add spent Time',
            command=self.on_save,
            font=ctk.CTkFont(family="Helvetica", size=15)
        )
        button_add_spent_time.grid(row=row, column=1, columnspan=10, pady=(20, 0))

        WindowHelper.size_and_center(self, resiz=False)
        self.autosize_columns()

    def autosize_columns(self) -> None:
        for col in self.item_time_list['columns']:
            self.item_time_list.column(col, width=ctk.CTkFont().measure(self.item_time_list.heading(col)['text']))
            for row in self.item_time_list.get_children(''):
                item_width = ctk.CTkFont().measure(self.item_time_list.set(row, col))
                self.item_time_list.column(col, width=max(self.item_time_list.column(col, 'width'), item_width))

    def load_item_times(self) -> None:
        for i in self.item_time_list.get_children():
            self.item_time_list.delete(i)

        item_times = self.time_management_window.selected_item.times

        for index, item_time in enumerate(item_times):
            item_id = self.item_time_list.insert(
                '',
                'end',
                values=(
                    DateTimeHelper.convert_datetime_to_string(item_time.record_date),
                    DateTimeHelper.convert_seconds_to_time_string(item_time.duration_seconds),
                    item_time.item_time_note,
                )
            )

            if index % 2 == 0:
                self.item_time_list.item(item_id, tags=('evenrow',))

        self.item_time_list.tag_configure('evenrow', background='#d3d3d3')

    def on_save(self):
        selected_date = self.date_picker.get_date()
        print(selected_date)
        selected_duration_hours = self.hour_spin_box.get_value()
        selected_duration_minutes = self.minute_spin_box.get_value()

        if not self.is_valid_input(selected_date, selected_duration_hours, selected_duration_minutes):
            Message.common_one_button_msg(
                'fail',
                'Invalid Input',
                'Please select a date or insert valid hours and minutes.'
            )
            return

        duration_seconds = DateTimeHelper.convert_to_seconds(
            int(selected_duration_hours),
            int(selected_duration_minutes)
        )

        record_date = DateTimeHelper.create_datetime_from_input(selected_date)

        if not self.is_valid_time_addition(record_date, duration_seconds):
            Message.common_one_button_msg(
                'fail',
                'Invalid Input',
                f'You cannot add such a value of time for {selected_date} '
                f'because the sum of assigned time would be longer than 24 hours.'
            )
            return

        note = self.note_entry.get()

        if self.verification_messagebox():
            self.save(record_date, duration_seconds, note)
            self.back_to_time_management_window()
        else:
            return

    def is_valid_input(self, date: str, hours: str, minutes: str) -> bool:
        return (
                date != ''
                and hours.isdigit()
                and int(hours) >= 0
                and minutes.isdigit()
                and int(minutes) >= 0
                and int(hours) + int(minutes) > 0
        )

    def is_valid_time_addition(self, date: datetime, duration_seconds: int) -> bool:
        item_times = self.time_management_window.selected_item.times
        cureent_item_time_daily = sum(
            item_time.duration_seconds for item_time in item_times if item_time.record_date == date
        )
        return cureent_item_time_daily + duration_seconds <= 86400

    def verification_messagebox(self) -> bool:
        msg_result = Message.show_msgbox(
            title='Do you really want to store the record for selected item?',
            message='Press OK to store the values or Cancel to dismiss',
            icon='warning',
            option_1=Const.yes,
            option_2=Const.no
        )

        if msg_result == Const.yes:
            return True
        return False

    def save(self, date_from: datetime, duration_seconds: int, note: str) -> None:
        result = self.controller.save_item_time(
            {
                'item_id': self.time_management_window.selected_item.item_id,
                'record_date': date_from,
                'duration_seconds': duration_seconds,
                'item_time_note': note
            }
        )

        Message.show_db_result(result, 'Item Time', Const.mode_add)

    def back_to_time_management_window(self):
        self.destroy()
        self.time_management_window.deiconify()
        self.time_management_window.grab_set()
