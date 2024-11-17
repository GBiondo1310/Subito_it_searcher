import customtkinter as ctk


class LabeledOptionsMenu(ctk.CTkFrame):
    """A frame which includes both a label and an option menu"""

    def __init__(self, master: ctk.CTkBaseClass, label: str, values: list[str]):
        """Initializes a new LabeledOptionsMenu instance

        :param master: The master widget
        :type master: ctk.CTkBaseClass
        :param label: The text of the label
        :type label: str
        :param values: A list of option to chose among
        :type values: list[str]
        """

        super().__init__(master)

        self.label = ctk.CTkLabel(self, text=label)
        self.label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        self.option_menu = ctk.CTkOptionMenu(self, values=values)
        self.option_menu.grid(row=1, column=0, padx=5, pady=(1, 10))

    def get(self) -> str:
        """Returns :func:``self.option_menu.get()``"""

        return self.option_menu.get()
