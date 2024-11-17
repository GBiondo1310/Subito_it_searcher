import customtkinter as ctk


class WarningDialog(ctk.CTkInputDialog):
    """A warning dialog which user can only accept"""

    def __init__(self, title: str, text: str):
        """Initializes a new WarningDialog instance

        :param title: The title of the dialog window
        :type title: str
        :param text: The main text of the dialog window
        :type text: str
        """

        super().__init__(title=title, text=text)
        self.after(11, self.clear)

    def clear(self):
        """Clears out unused :func:``ctk.CTkInputDialog`` widgets"""
        self._entry.grid_forget()
        self._cancel_button.grid_forget()
