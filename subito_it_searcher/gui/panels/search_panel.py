import tkinter as tk
import os

import customtkinter as ctk

from .main_panel import MainPanel

from ..widgets.labeled_entry import LabeledEntry
from ..widgets.labeled_option_menu import LabeledOptionsMenu
from ..widgets.warning_dialog import WarningDialog

from ...classes.searcher import Searcher, Advertisement
from ..._funcs import get_favorites, purge_pictures


class SearchPanel(ctk.CTkFrame):
    """Search frame
    User can input search parameters"""

    def __init__(self, master):
        """Initialization function"""

        super().__init__(master=master)

        self.search_entry = LabeledEntry(self, "Ricerca", "Articolo")
        self.search_entry.grid(row=0, column=0, padx=5, pady=10)
        self.search_entry.on_return(self.search)

        self.ads_number_entry = LabeledEntry(self, "Risultati", "100")
        self.ads_number_entry.grid(row=1, column=0, padx=5, pady=10)
        self.ads_number_entry.on_return(self.search)

        self.min_price_entry = LabeledEntry(self, "Prezzo minimo", "0")
        self.min_price_entry.grid(row=2, column=0, padx=5, pady=10)
        self.min_price_entry.on_return(self.search)

        self.max_price_entry = LabeledEntry(self, "Prezzo Massimo", "0")
        self.max_price_entry.grid(row=3, column=0, padx=5, pady=10)
        self.max_price_entry.on_return(self.search)

        self.order_by_menu = LabeledOptionsMenu(
            self, "Ordina per", ["Data", "Prezzo crescente", "Prezzo descrescente"]
        )
        self.order_by_menu.grid(row=4, column=0, padx=5, pady=10)

        self.match_exact_search = ctk.CTkSwitch(self, text="Match exact text")
        self.match_exact_search.grid(row=5, column=0, padx=5, pady=10, sticky="w")

        self.exclude_blacklisted_sellers = ctk.CTkSwitch(
            self, text="Exclude blacklisted sellers"
        )
        self.exclude_blacklisted_sellers.grid(
            row=6, column=0, padx=5, pady=10, sticky="w"
        )

        self.exclude_past_ads = ctk.CTkSwitch(self, text="Exclude past ads")
        self.exclude_past_ads.grid(row=7, column=0, padx=5, pady=10, sticky="w")

        self.exclude_sold_items = ctk.CTkSwitch(self, text="Exclude sold items")
        self.exclude_sold_items.grid(row=8, column=0, padx=5, pady=10, sticky="w")

        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.search_button = ctk.CTkButton(self, text="SEARCH", command=self.search)
        self.search_button.grid(row=9, column=0, padx=5, pady=10)

        self.favorites_button = ctk.CTkButton(
            self, text="Favorites", command=self.show_favorites
        )
        self.favorites_button.grid(row=10, column=0, padx=5, pady=10)

    def search(self, *e):
        """Makes the research and updates the main frame"""
        if self.input_control():
            self.master.main_panel.destroy()

            purge_pictures()

            def go_on():

                max_price = (
                    int(self.max_price_entry.get())
                    if self.max_price_entry.get().isnumeric()
                    else None
                )
                min_price = (
                    int(self.min_price_entry.get())
                    if self.min_price_entry.get().isnumeric()
                    else None
                )

                searcher = Searcher(
                    self.search_entry.get(),
                    int(self.ads_number_entry.get()),
                    self.order_by,
                    min_price,
                    max_price,
                    self.match_exact_search.get(),
                    self.exclude_blacklisted_sellers.get(),
                    self.exclude_past_ads.get(),
                    self.exclude_sold_items.get(),
                )

                mf = MainPanel(self.master, self.search_entry.get(), searcher.ads)
                self.master.main_panel = mf
                mf.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

            self.after(10, go_on)

    def input_control(self) -> bool:
        """Checks user input"""
        if not self.search_entry.get():
            WarningDialog("Missing input", "Please insert search terms")
            self.search_entry.focus_set()
            return False

        if not self.ads_number_entry.get():
            WarningDialog("Missing input", "Please insert ads amount (min 100)")
            self.ads_number_entry.set()
            return False

        if not self.ads_number_entry.get().isnumeric():
            WarningDialog("Wrong input", "Ads number must be an integer number")
            self.ads_number_entry.focus_set()
            return False

        if int(self.ads_number_entry.get()) < 100:
            WarningDialog("Wrong input", "Must search at lease 100 ads")
            self.ads_number_entry.focus_set()
            return False

        if self.min_price_entry.get():
            if not self.min_price_entry.get().isnumeric():
                WarningDialog(
                    "Wrong input", "Minimum price must be a floating point number"
                )
                self.min_price_entry.focus_set()
                return False

        if self.max_price_entry.get():
            if not self.max_price_entry.get().isnumeric():
                WarningDialog(
                    "Wrong input", "Maximum price must be a floating point number"
                )
                self.max_price_entry.focus_set()
                return False

        return True

    @property
    def order_by(self):
        match self.order_by_menu.get():
            case "Prezzo crescente":
                return "lowest price"
            case "Prezzo descrescente":
                return "highest price"
            case "Data":
                return "date"

    @property
    def min_price(self):
        if not self.min_price_entry.get():
            return 0

    @property
    def max_price(self):
        if not self.max_price_entry.get():
            return 99999

    def show_favorites(self):
        """Displays all favorites Advertisements"""
        self.master.main_panel.destroy()

        purge_pictures()

        ads = []

        for key, ad in get_favorites().items():
            ads.append(Advertisement(ad))

        mf = MainPanel(self.master, "Favorites", ads)
        self.master.main_panel = mf
        mf.grid(row=0, column=1, padx=10, pady=10, sticky="nsnwe")
