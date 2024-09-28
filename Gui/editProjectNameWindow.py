import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session

from models import Project


class EditProjectNameWindow(tk.Toplevel):
    width = 370
    height = 150

    def __init__(self, parent: tk.Toplevel, session: Session, project: Project, refresh_project_list):
        super().__init__(parent)
        self.title('Edit Project Name')
        self.session = session
        self.project = project
        self.refresh_project_list = refresh_project_list
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.project_name_var = tk.StringVar(value=self.project.project_name)
        self.create_window_objects()

    def create_window_objects(self):
        self.project_name_label = tk.Label(self, text="Project Name")
        self.project_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.project_name_entry = tk.Entry(self, textvariable=self.project_name_var, width=40)
        self.project_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.save_button = tk.Button(self, text="Save and Close", command=self.save_project_name)
        self.save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def save_project_name(self):
        new_project_name = self.project_name_var.get()

        if not new_project_name.strip():
            messagebox.showwarning("Validation Error", "Project name cannot be empty.")
            return

        self.project.project_name = new_project_name

        try:
            self.session.commit()
            messagebox.showinfo("Success", "Project name updated successfully!")
            self.refresh_project_list()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update project: {e}")
            self.session.rollback()
