import unittest
import json

from subito_it_searcher.classes.advertisement import Advertisement


class TestAdvertisement(unittest.TestCase):
    """Test Advertisement class"""

    def test_ad(self):
        with open("tests/test_ad.json", mode="r") as test_ad_file:
            ad = json.load(test_ad_file)
        advertisement = Advertisement(ad)
        self.assertEqual(advertisement.ad_id, "577477491")
        self.assertEqual(advertisement.title, "Artillery Swx2")
        self.assertEqual(
            advertisement.description,
            "vendo per inutilizzo stampante 3d artillery Swx2 ancora in garanzia con modifiche barre laterali pi\u00f9 piatto in pei con poche ore di stampa pi\u00f9 qualche pezzo di ricambio acquistato a parte ",
        )
        self.assertEqual(advertisement.pubblication_date.day, 10)
        self.assertEqual(advertisement.selling_price, 200)
        self.assertEqual(advertisement.shipping_price, 50)
        self.assertEqual(
            advertisement.url,
            "https://www.subito.it/informatica/artillery-swx2-bari-577477491.htm",
        )
