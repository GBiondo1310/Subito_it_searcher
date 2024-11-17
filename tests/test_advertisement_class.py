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
            "vendo per inutilizzo stampante 3d artillery Swx2"
            in advertisement.description,
            True,
        )
        self.assertEqual(advertisement.pubblication_date.day, 10)
        self.assertEqual(advertisement.selling_price, 200)
        self.assertEqual(advertisement.shipping_price, 50)
        self.assertEqual(
            advertisement.url,
            "https://www.subito.it/informatica/artillery-swx2-bari-577477491.htm",
        )
