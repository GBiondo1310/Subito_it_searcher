import tkinter as tk
import customtkinter as ctk

from ...classes.advertisement import Advertisement

from ..widgets.ad_expanding_card import AdExpandingCard


class MainPanel(ctk.CTkFrame):
    """Main panel of the GUI
    Found ads will be placed here"""

    def __init__(self, master, search, results):

        super().__init__(master=master)

        self.current_ad_group_index = 0
        self.results = results
        self.ad_groups = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.search_label = ctk.CTkLabel(
            self, text=f"Results for: {search}", anchor="center", font=(None, 25)
        )
        self.search_label.grid(row=0, column=0, padx=10, sticky="nswe")

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid(row=1, column=0, pady=10, sticky="nswe")

        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nswe")

        self.next_button = ctk.CTkButton(
            self.footer_frame, text="Next", command=self.next_group
        )
        self.next_button.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")

        self.prev_button = ctk.CTkButton(
            self.footer_frame, text="Prev", command=self.prev_group
        )
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.number_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"Page {self.current_ad_group_index + 1} of {len(self.ad_groups)}",
        )
        self.number_label.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")

        self.group_results_by(10)
        self.place_ad_group(self.current_ad_group_index)

    def group_results_by(self, group_dimension: int):
        """Groups the ads retreived from Subito.it in groups of
        ``{group_dimension}`` entries

        :param group_dimension: The dimension of every ads group
        :type group_dimension: int"""

        self.ad_groups = [
            [
                AdExpandingCard(self.scroll_frame, result, index)
                for index, result in enumerate(self.results[i : i + group_dimension])
            ]
            for i in range(0, len(self.results), group_dimension)
        ]

    def forget_ad_group_grid(self, group_index: int):
        """Removes widgets that are in a specific ads group

        :param group_index: The index of the ads group
        :type group_index: int
        """

        for ad in self.ad_groups[group_index]:
            ad.grid_forget()

    def place_ad_group(self, group_index: int):
        """Places widgets that are in a specific ads group

        :param group_index: The index of the ads group
        :type groupd index: int"""

        if any(self.results):
            for ad in self.ad_groups[group_index]:
                ad.auto_place()

    def next_group(self, *e):
        """Removes current group's ads and places next group ads"""
        if self.current_ad_group_index < len(self.ad_groups) - 1:
            self.forget_ad_group_grid(self.current_ad_group_index)

            self.current_ad_group_index += 1

            self.number_label.configure(
                text=f"Page {self.current_ad_group_index + 1} of {len(self.ad_groups)}"
            )
            self.place_ad_group(self.current_ad_group_index)

    def prev_group(self, *e):
        """Removes current group's ads and places previous group ads"""
        if self.current_ad_group_index > 0:
            self.forget_ad_group_grid(self.current_ad_group_index)

            self.current_ad_group_index -= 1

            self.number_label.configure(
                text=f"Page {self.current_ad_group_index + 1} of {len(self.ad_groups)}"
            )

            self.place_ad_group(self.current_ad_group_index)

    def destroy(self):
        for group in self.ad_groups:
            for ad in group:
                ad.destroy()
        return super().destroy()
