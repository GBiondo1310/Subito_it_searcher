import unittest
import os

from subito_it_searcher._funcs import (
    get_image,
    get_past_ads,
    get_users_blacklist,
    add_past_ads,
    add_user_to_blacklist,
)


class TestFunc(unittest.TestCase):
    """Test _funcs.py"""

    def create_test_picture_dir(self):
        os.mkdir("test_pictures")

    def delete_test_picture_dir(self):
        os.system("rm test_pictures/test.jpg")
        os.rmdir("test_pictures")

    def test_get_image(self):
        # TODO - Change this image if no longer on Subito.it database in the future
        self.create_test_picture_dir()
        image = "https://images.sbito.it/api/v1/sbt-ads-images-pro/images/9f/9fe0c338-3d68-4526-8b18-69ea056017d3?rule=thumbs-auto"
        get_image(image, "test_pictures/test.jpg")
        self.assertIn("test.jpg", os.listdir("test_pictures"))
        self.delete_test_picture_dir()

    def test_get_past_ads(self):
        self.assertIsInstance(get_past_ads(), list)

    def test_get_users_blacklist(self):
        self.assertIsInstance(get_users_blacklist(), list)

    def test_add_past_ads(self):
        add_past_ads("1111")
        self.assertGreater(len(get_past_ads()), 0)

    def test_add_user_to_blacklist(self):
        add_user_to_blacklist("123456")
        self.assertGreater(len(get_users_blacklist()), 0)
