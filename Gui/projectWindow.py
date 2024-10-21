import customtkinter as ctk

from helpers.constants import Constants as Const
from helpers.dataValidation import DataValidation
from helpers.message import Message
from helpers.windowHelper import WindowHelper
from models import Project


class ProjectWindow(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, entity_name: str, controller, mode: str):
        super().__init__(parent)
        self.entity_name = entity_name
        self.controller = controller
        self.mode = mode
        self.customers = self.controller.get_active_customers()
        self.customer_map = {}
        self.selected_customer = None
        self.selected_project = None

        self.fields = {
            'project_name': (ctk.StringVar(), 'Project Name')
        }

        self.setup_window()
        self.create_window_objects()

    def setup_window(self) -> None:
        self.title(WindowHelper.get_title(self.entity_name, self.mode))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

    def create_window_objects(self) -> None:
        self.create_customer_selection()
        if self.mode in [Const.mode_edit, Const.mode_delete]:
            self.create_project_selection()
        if self.mode in [Const.mode_add, Const.mode_edit]:
            self.create_project_name_entry()
        self.create_submit_button()
        WindowHelper.size_and_center(self, resiz=False)
        self.load_combo_customers()

    def create_customer_selection(self) -> None:
        ctk.CTkLabel(self, text='Customer').grid(row=0, column=1, padx=0, pady=(20, 0), sticky='SW')
        self.customer_combobox = ctk.CTkComboBox(
            self,
            state="readonly",
            width=500,
            command=self.on_customer_select,
            values=[]
        )
        self.customer_combobox.grid(row=1, column=1, padx=0, pady=(0, 15), sticky='NW')

    def create_project_selection(self) -> None:
        ctk.CTkLabel(self, text='Project').grid(row=2, column=1, padx=0, pady=0, sticky='SW')
        self.project_combobox = ctk.CTkComboBox(
            self,
            state='disabled',
            width=500,
            command=self.on_project_select,
            values=[]
        )
        self.project_combobox.grid(row=3, column=1, padx=0, pady=(0, 15), sticky='NW')

    def create_project_name_entry(self) -> None:
        label_text = 'New Project Name' if self.mode == Const.mode_edit else 'Project Name'
        ctk.CTkLabel(self, text=label_text).grid(row=4, column=1, padx=0, pady=0, sticky='SW')
        self.project_name_entry = ctk.CTkEntry(
            self,
            textvariable=self.fields['project_name'][0],
            width=500,
            state='disabled'
        )
        self.project_name_entry.grid(row=5, column=1, padx=0, pady=(0, 15), sticky='NW')

    def create_submit_button(self) -> None:
        button_text = {
            Const.mode_add: 'Save Project',
            Const.mode_edit: 'Update Project',
            Const.mode_delete: 'Delete Project'
        }.get(self.mode, 'Submit')

        ctk.CTkButton(
            self,
            text=button_text,
            command=self.submit,
            font=ctk.CTkFont(family="Helvetica", size=15)
        ).grid(row=6, column=1, pady=(20, 0))

    def load_combo_customers(self) -> None:
        self.create_customer_map()
        self.customer_combobox.configure(values=list(self.customer_map.keys()))

    def create_customer_map(self) -> None:
        for customer in self.customers:
            customer_name = (
                f'{customer.company_name + ", " if customer.company_name is not None else ""} '
                f'{customer.first_name} {customer.last_name}, '
                f'{customer.street} {str(customer.street_number)}, {customer.city}'
            )
            self.customer_map[customer_name] = customer

    def on_customer_select(self, event=None) -> None:
        self.selected_customer = self.customer_map.get(self.customer_combobox.get())
        self.clear_fields()

        if self.selected_customer is not None and self.mode in [Const.mode_edit, Const.mode_delete]:
            self.load_projects_for_selected_customer()

        if self.mode == Const.mode_add:
            self.project_name_entry.configure(state='normal')

    def load_projects_for_selected_customer(self) -> None:
        project_names = [
            project.project_name for project in self.selected_customer.projects if project.status == Const.status_active
        ]

        WindowHelper.reset_combobox(self.project_combobox, project_names)

    def clear_fields(self) -> None:
        for var, _ in self.fields.values():
            var.set('')

    def on_project_select(self, event=None) -> None:
        self.selected_project = self.get_selected_project(self.project_combobox.get())

        if self.selected_project is not None and self.mode != Const.mode_delete:
            self.fields.get('project_name')[0].set(self.selected_project.project_name)
            self.project_name_entry.configure(state='normal')

    def get_selected_project(self, selected_project_name: str) -> Project | None:
        if self.selected_customer is not None:
            for project in self.selected_customer.projects:
                if project.project_name == selected_project_name:
                    return project
        return None

    def submit(self) -> None:
        if not self.validate_selection():
            return

        validated_data = DataValidation.validate_data(Project, self.fields) if self.mode != Const.mode_delete else ''

        if validated_data is None:
            return

        match self.mode:
            case Const.mode_add:
                result = self.on_add(validated_data)
            case Const.mode_edit:
                result = self.on_edit(validated_data)
            case Const.mode_delete:
                result = self.on_delete()
            case _:
                raise ValueError('Mode not recognised.')

        if result is not None:
            Message.show_db_result(result, 'Project', self.mode)

        self.grab_release()
        self.destroy()

    def validate_selection(self) -> bool:
        if self.mode == Const.mode_add and self.selected_customer is None:
            Message.common_one_button_msg('fail', 'Invalid Input', 'Please select a customer.')
            return False

        if self.mode in [Const.mode_edit, Const.mode_delete] and self.selected_project is None:
            Message.common_one_button_msg('fail', 'Invalid Input', f'Please select a project to {self.mode}.')
            return False

        return True

    def on_add(self, validated_data: dict) -> bool:
        validated_data['customer_id'] = self.selected_customer.customer_id
        return self.controller.save_project(validated_data)

    def on_edit(self, validated_data: dict) -> bool:
        return self.controller.update_project(self.selected_project, validated_data)

    def on_delete(self) -> bool | None:
        msg_result = Message.show_msgbox(
            title='Do you really want to delete selected project?',
            message='If you delete a project, all its related items will be deleted as well.',
            icon='warning',
            option_1=Const.yes,
            option_2=Const.no
        )

        if msg_result == Const.yes:
            return self.controller.delete_project_and_all_items(self.selected_project)

        return None
