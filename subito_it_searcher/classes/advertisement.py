from datetime import datetime

from .._consts import SUBITO_DATE_FORMAT
from .._funcs import (
    add_user_to_blacklist,
    add_past_ads,
    add_to_favorites,
    remove_from_favorites,
    get_favorites,
)


class Advertisement:
    """Class that parses an advertisement from Subito.it"""

    def __init__(self, subito_object: dict):
        """Initializes a new SubitoObjectParses instance

        :param subito_object: An object retreived in the response from Subito.it
        :type subito_object: dict
        """
        self._obj = subito_object

    def __str__(self) -> str:
        """String representation
        :rtype: str"""
        return str(self.selling_price)

    @property
    def ad_id(self) -> str:
        """Returns object advertisement's id

        :rtype: str"""
        return self._obj.get("urn").split(":list:")[1]

    @property
    def title(self) -> str:
        """Returns object advertisement's title

        :rtype: str
        """
        return self._obj.get("subject")

    @property
    def description(self) -> str:
        """Returns object advertisement's description

        :rtype: str
        """
        return self._obj.get("body")

    @property
    def pubblication_date(self) -> datetime:
        """Returns object advertisement's pubblication date

        :rtype: str
        """
        return datetime.strptime(
            self._obj.get("dates").get("display"), SUBITO_DATE_FORMAT
        )

    @property
    def selling_price(self) -> float:
        """Returns object's selling price

        :rtype: float"""
        for feature in self._obj.get("features"):
            if feature.get("label") == "Prezzo":
                return float(feature.get("values")[0].get("key").replace(",", "."))

    @property
    def shipping_price(self) -> float:
        """Returns object's shipping price

        :rtype: float
        """
        for feature in self._obj.get("features"):
            if feature.get("label") == "Costo della spedizione":
                return float(feature.get("values")[0].get("key").replace(",", "."))

    @property
    def sold(self) -> bool:
        for feature in self._obj.get("features"):
            if feature.get("values")[0].get("value") == "SOLD":
                return True
        return False

    @property
    def user_id(self) -> str:
        """Returns advertisement's user id

        :rtype: float"""
        return self._obj.get("advertiser").get("user_id")

    @property
    def url(self) -> str:
        """Returns advertisement's Subito.it id

        :rtype: str"""
        return self._obj.get("urls").get("default")

    @property
    def images(self) -> list[str]:
        """Returns a list of images links

        :rtype: list[str]"""
        images = []
        for image in self._obj.get("images"):
            url = image.get("cdn_base_url") + "?rule=bigcardimages-auto"
            images.append(url)

        return images

    @property
    def is_favorite(self) -> bool:
        """Returns wether ``self._obj`` has been stored in favorites or not

        :rtype: bool"""
        favorites = get_favorites()
        if self.ad_id in favorites.keys():
            return True
        return False

    def add_user_to_blacklist(self):
        """Adds advertisement's user to blacklisted users"""

        add_user_to_blacklist(self.user_id)

    def add_to_past_ads(self):
        """Adds this advertisement to past ads"""

        add_past_ads(self.ad_id)

    def add_to_favorites(self):
        """Adds this Ad to favorites"""

        add_to_favorites(self._obj)

    def remove_from_favorites(self):
        """Removes this Ad from favorites"""
        remove_from_favorites(self._obj)
