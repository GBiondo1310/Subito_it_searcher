import customtkinter as ctk
from tkinter import StringVar


class LabeledEntry(ctk.CTkFrame):
    """A frame which includes both a label and an entry field"""

    def __init__(self, master: ctk.CTkBaseClass, label: str, hint: str):
        """Initializes a new LabeledEntry instance

        :param master: The master widget
        :type master: ctk.CTkBaseClass
        :param label: The label text
        :type label: str
        :param hint: The entry hint text
        :type hint: str
        """

        super().__init__(master)

        self.label = ctk.CTkLabel(self, text=label)
        self.label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        self.entry = ctk.CTkEntry(self, placeholder_text=hint)
        self.entry.grid(row=1, column=0, padx=5, pady=(1, 10))

    def on_return(self, callback):
        """Binds Return key to a callback"""
        self.entry.bind("<Return>", callback)

    def get(self) -> str:
        """Returns :func:``self.entry.get()``"""
        return self.entry.get()
