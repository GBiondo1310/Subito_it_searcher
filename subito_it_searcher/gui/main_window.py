import customtkinter as ctk

# TEST
import json
from .widgets.ad_expanding_card import AdExpandingCard
from ..classes.advertisement import Advertisement


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
        # self.grid_rowconfigure(0, weight=1)

        # TEST

        with open("tests/test_ad.json", mode="r") as test_ad_file:
            ad = json.load(test_ad_file)

        advertisement = Advertisement(ad)

        self.ad = AdExpandingCard(self, advertisement)
        self.ad.grid(row=0, column=1, padx=10, pady=5, sticky="nswe")

        self.ad2 = AdExpandingCard(self, advertisement)
        self.ad2.grid(row=1, column=1, padx=10, pady=5, sticky="nswe")
