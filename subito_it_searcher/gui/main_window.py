import customtkinter as ctk
from .widgets.labeled_entry import LabeledEntry


class GUI(ctk.CTk):
    """Main GUI window"""

    def __init__(self):
        """Initializes the GUI"""
        super().__init__()
        self.title("Subito.it searcher")
        self.geometry("1600x900")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        LabeledEntry(self, "asd", "test").grid(row=0, column=0)
