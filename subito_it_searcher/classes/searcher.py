from ..alebrandi.subito import Subito
from .advertisement import Advertisement
from .._funcs import get_users_blacklist, get_past_ads


class Searcher(Subito):
    """Searcher class implemented from alebrandi's Subito class.
    Fetches, parses and filters Subito.it ads"""

    def __init__(
        self,
        search_item: str,
        results_number: int = 100,
        order_by: str = "date",
        min_price: float = None,
        max_price: float = None,
        match_exact_item: bool = False,
        exclude_blacklisted_users: bool = False,
        exclude_past_ads: bool = False,
        exclude_sold_items: bool = False,
    ):
        """Initializes a new Searcher instance

        :param search_item: The name of the item to search
        :type search_item: str
        :param results_number: The number of results to fetch (minimum 100), defaults to 100
        :type results_number: int, optional
        :param order_by: Order by type, can be "date, lowest price" or "highest price", defaults to "lowest price"
        :type order_by: str, optional
        :param min_price: Minimum price filter, if None will be set to 0 defaults to None
        :type min_price: float, optional
        :param max_price: Maximum price filter, if None will be set to 999999, defaults to None
        :type max_price: float, optional
        :param match_exact_item: Title or description MUST have the search term in their content, defaults to False
        :type match_exact_item: bool, optional
        :param exclude_blacklisted_users: Exclude blacklisted user's ads, defaults to False
        :type exclude_blacklisted_users: bool, optional
        :param exclude_past_ads: Exclude ads which were already fetched in past searches, defaults to False
        :type exclude_past_ads: bool, optional
        :param exclude_sold_items: Exclude items that are already marked as sold, defaults to False
        :type exclude_sold_items: bool, optional
        """

        super().__init__(search_item=search_item)

        self.results_number = results_number
        self.order_by = order_by
        self.match_exact_search = match_exact_item
        self.exclude_blacklisted_users = exclude_blacklisted_users
        self.exclude_past_ads = exclude_past_ads
        self.exclude_sold_items = exclude_sold_items
        self.min_price = min_price if min_price else 0
        self.max_price = max_price if max_price else 999999

        _ads = [
            Advertisement(result)
            for result in self.search(
                results=self.results_number, sort_by=self.order_by
            )
        ]

        self.ads: list[Advertisement] = [
            result for result in _ads if self.ad_matches_filters(result)
        ]

        self.sort_ads_by_price_desc()

    def ad_matches_filters(self, ad: Advertisement) -> bool:
        """Checks if the passed Advertisement matches search filters

        :param ad: The Advertisement instance to check
        :type ad: Advertisement

        :rtype: bool
        """

        if self.match_exact_search:
            title = ad.title.replace(" ", "").lower()
            description = ad.title.replace(" ", "").lower()
            search_item = self.search_item.replace(" ", "").lower()
            if search_item not in title and search_item not in description:
                return False

        if self.exclude_blacklisted_users:
            if ad.user_id in get_users_blacklist():
                return False

        if self.exclude_past_ads:
            if ad.ad_id in get_past_ads():
                return False

        if self.exclude_sold_items:
            if ad.sold:
                return False

        if self.min_price:
            if not ad.selling_price:
                return False
            if ad.selling_price < self.min_price:
                return False

        if self.max_price:
            if not ad.selling_price:
                return False
            if ad.selling_price > self.max_price:
                return False
        return True

    def sort_ads_by_price_asc(self):
        """Sorts ``self.ads`` by price ascending"""

        def return_price(ad: Advertisement):
            return ad.selling_price

        self.ads.sort(key=return_price)

    def sort_ads_by_price_desc(self):
        """Sorts ``self.ads`` by price descending"""

        def return_price(ad: Advertisement):
            return ad.selling_price

        self.ads.sort(key=return_price)
