import tkinter as tk
import webbrowser
from PIL import Image

import customtkinter as ctk
from ...classes.advertisement import Advertisement
from ..._funcs import (
    get_image,
    add_user_to_blacklist,
    add_past_ads,
    get_past_ads,
    get_users_blacklist,
    remove_user_from_blacklist,
    remove_from_past_ads,
)


class AdExpandingCard(ctk.CTkFrame):
    """Advertisement collapsing card"""

    def __init__(self, master: ctk.CTkBaseClass, ad: Advertisement, row: int = 0):
        """Initializes a new AdExpandingCard instance

        :param master: The master widget
        :type master: ctk.CTkBaseClass
        :param ad: The Advertisement to visualize
        :type ad: Advertisement
        :param row: The master widget's grid row in which place this instance, defaults to 0
        :type row: int, optional
        """

        super().__init__(master)

        self.image_downloaded = False

        self.ad = ad
        self.expanded = tk.BooleanVar()
        self.expanded.trace_add("write", self.expand)

        self.grid_rowconfigure(1, weight=1)  # BODY FRAME WILL EXPAND
        self.grid_columnconfigure(0, weight=1)

        # ----- HEADER FRAME ----- #

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nswe")

        self.expand_switch = ctk.CTkSwitch(
            self.header_frame, text="Expand", variable=self.expanded, font=(None, 15)
        )
        self.expand_switch.grid(row=0, column=0, padx=20, sticky="w")

        self.title_label = ctk.CTkLabel(
            self.header_frame, text=ad.title, font=(None, 20)
        )
        self.title_label.grid(row=0, column=1, pady=10, sticky="nswe")

        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text=f"{self.ad.pubblication_date}   |   {self.ad.selling_price}€",
            font=(None, 15),
        )
        self.date_label.grid(row=0, column=2, padx=20)

        # ----- BODY FRAME ----- #

        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid_columnconfigure(0, weight=1)
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid(row=1, column=0, padx=20, pady=1, sticky="nswe")

        self.description_label = ctk.CTkLabel(
            self.body_frame,
            text=ad.description,
            justify=tk.LEFT,
            anchor="nw",
            font=(None, 15),
            wraplength=1000,
        )
        self.description_label.grid(row=0, column=0, padx=20, pady=10, sticky="nswe")

        self.outer_image_frame = ctk.CTkFrame(self.body_frame)
        self.outer_image_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nswe")

        self.show_images_variable = tk.Variable(value=False)
        self.show_images_variable.trace_add(mode="write", callback=self.download_images)

        self.show_images_switch = ctk.CTkSwitch(
            self.outer_image_frame,
            text="Show images",
            variable=self.show_images_variable,
        )
        self.show_images_switch.grid(row=0, column=0, padx=20, pady=10, sticky="nse")

        self.inner_image_frame = ctk.CTkFrame(self.outer_image_frame)

        # ----- FOOTER FRAME ----- #
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid_rowconfigure(0, weight=1)

        self.user_blacklisted = (
            True if self.ad.user_id in get_users_blacklist() else False
        )
        self.ad_in_past_ads = True if self.ad.ad_id in get_past_ads() else False

        self.user_action = ctk.CTkButton(
            self.footer_frame,
            text=(
                "Remove user from blacklist"
                if self.user_blacklisted
                else "Add user to blacklist"
            ),
            command=self.blacklist_user,
        )
        self.ad_action = ctk.CTkButton(
            self.footer_frame,
            text=(
                "Remove advertisement from past ads"
                if self.ad_in_past_ads
                else "Add adadvertisement to past ads"
            ),
            command=self.add_past_ad,
        )
        self.open_link_button = ctk.CTkButton(
            self.footer_frame, text="View in browser", command=self.open_link
        )

        self.expanded.set(False)

        self.user_action.grid(row=0, column=0, padx=10, pady=2, sticky="nswe")
        self.ad_action.grid(row=0, column=1, padx=10, pady=2, sticky="nswe")
        self.open_link_button.grid(row=0, column=2, padx=10, pady=2, sticky="nswe")

        self.row = row

    def __str__(self) -> str:
        """String representation
        :rtype: str"""
        return f"AEC {self.ad.ad_id}"

    def __repr__(self) -> str:
        return self.__str__()

    def expand(self, *e):
        """Expands the ad card"""
        if self.expanded.get():
            self.body_frame.grid(row=1, column=0, padx=20, pady=1, sticky="nswe")
            self.outer_image_frame.grid(row=0, column=1, padx=5, pady=2, sticky="nswe")
            self.footer_frame.grid(row=2, column=0, padx=20, pady=1, sticky="nswe")

        else:
            self.body_frame.grid_forget()
            self.outer_image_frame.grid_forget()
            self.footer_frame.grid_forget()

    def download_images(self, *e):
        """Downloads and displays the first image of the ad"""
        if not self.show_images_variable.get():
            self.inner_image_frame.grid_forget()
        else:
            self.inner_image_frame.grid(row=1, column=0, padx=20, pady=10)

        if not self.image_downloaded:
            with open("pictures/index.txt", mode="r") as index_file:
                index = int(index_file.read())

            get_image(self.ad.images[0], f"pictures/{index}.png")
            img = ctk.CTkImage(Image.open(f"pictures/{index}.png"), size=(400, 400))
            index += 1

            imgLabel = ctk.CTkLabel(self.inner_image_frame, image=img, text="")
            imgLabel.grid(row=2, column=0, padx=5, sticky="nswe")

            with open("pictures/index.txt", mode="w") as index_file:
                index_file.write(str(index))

            self.image_downloaded = True

    def blacklist_user(self, *e):
        """Adds or removes seller to the users blacklist"""
        self.user_blacklisted = not self.user_blacklisted
        if self.user_blacklisted:
            self.user_action.configure(text="Add user blacklist")
            remove_user_from_blacklist(self.ad.user_id)
        else:
            self.user_action.configure(text="Remove user from blacklist")
            add_user_to_blacklist(self.ad.user_id)

    def add_past_ad(self, *e):
        """Adds or removes ad to past ads"""

        if self.ad_in_past_ads:
            self.ad_action.configure(text="Remove advertisement from past ads")
            remove_from_past_ads(self.ad.ad_id)
        else:
            self.ad_action.configure(text="Add advertisement to past ads")
            add_past_ads(self.ad.ad_id)
        self.ad_in_past_ads = not self.ad_in_past_ads

    def auto_place(self):
        """Function to quickly place this widget using the :func:``self.row``property"""
        self.grid(row=self.row, column=0, padx=10, pady=5, sticky="nswe")
        self.ad.add_to_past_ads()

    def open_link(self, *e):
        """Opens the ad's link in a browser"""
        webbrowser.open(self.ad.url, new=2)
