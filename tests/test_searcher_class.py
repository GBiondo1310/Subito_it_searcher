import unittest

from subito_it_searcher.classes.searcher import Searcher


class TestSearcher(unittest.TestCase):
    """Test Searcher"""

    def test_search(self):
        searcher = Searcher("Stampante 3D", 100, min_price=50, max_price=80)

        self.assertLess(len(searcher.ads), 100)
        for ad in searcher.ads:
            self.assertGreaterEqual(ad.selling_price, 50)
            self.assertLessEqual(ad.selling_price, 80)
