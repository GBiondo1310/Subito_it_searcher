import wget
import json
import os


def get_image(image_url: str, out: str):
    """Downloads an image relative to an ad and places it in "pictures" folder

    :param image_url: The url of the image
    :type image_url: str
    :param out: The output name of the downloaded picture
    :type out: str
    """
    wget.download(image_url, out=out)


def get_past_ads() -> list[str]:
    """Gets the ad's ID of past ads

    :rtype: list[str]"""
    with open("history.json", mode="r") as history_file:
        history = json.load(history_file)

    return history.get("past_ads")


def get_users_blacklist() -> list[str]:
    """Gets the user's ID ot the users blacklist

    :rtype: list[str]"""
    with open("history.json", mode="r") as history_file:
        history = json.load(history_file)

    return history.get("users_blacklist")


def add_past_ads(ad_id: str):
    """Adds the passed ad's id to the past ads history

    :param ad_id: The id of the ad to add to the past_ad_history
    :type ads: str"""

    past_ads = get_past_ads()
    if ad_id not in past_ads:
        past_ads.append(ad_id)

        with open("history.json", mode="r") as history_file:
            history = json.load(history_file)

        history.update({"past_ads": past_ads})

        with open("history.json", mode="w") as history_file:
            json.dump(history, history_file, indent=4)


def remove_from_past_ads(ad_id: str):
    """Removes the passed ad's id from the past ads history

    :param ad_id: The id of the ad to remove from the past ads history
    :type ad_id: str"""

    past_ads = get_past_ads()
    if ad_id in past_ads:
        past_ads.remove(ad_id)
        with open("history.json", mode="r") as history_file:
            history = json.load(history_file)

        history.update({"past_ads": past_ads})

        with open("history.json", mode="w") as history_file:
            json.dump(history, history_file, indent=4)


def add_user_to_blacklist(user_id: str):
    """Adds the passed user's id to the user's blacklist

    :param user_id: The id of the user to add to the blacklist
    :type user_id: str"""
    users_blacklist = get_users_blacklist()
    if user_id not in users_blacklist:
        users_blacklist.append(user_id)

        with open("history.json", mode="r") as history_file:
            history = json.load(history_file)

        history.update({"users_blacklist": users_blacklist})

        with open("history.json", mode="w") as history_file:
            json.dump(history, history_file, indent=4)


def remove_user_from_blacklist(user_id: str):
    """Removes user from blacklist if user in blacklist

    :param user_id: The id of the user to remove from the blacklist
    :type user_id: str"""

    users_blacklist = get_users_blacklist()
    if user_id in users_blacklist:
        users_blacklist.remove(user_id)

        with open("history.json", mode="r") as history_file:
            history = json.load(history_file)

        history.update({"users_blacklist": users_blacklist})

        with open("history.json", mode="w") as history_file:
            json.dump(history, history_file, indent=4)


def get_favorites() -> dict:
    """Returns advertisement in favorites

    :rtype: dict"""
    with open("history.json", mode="r") as history_file:
        history = json.load(history_file)

    return history.get("favorites")


def add_to_favorites(advertisement: dict):
    """Adds an ad to favorites

    :param advertisement: The advertisement to add to the favorites
    :type advertisement: dict"""
    ad_id = advertisement.get("urn").split(":list:")[1]
    with open("history.json", mode="r") as history_file:
        history = json.load(history_file)

    favorites: dict = history.get("favorites")

    if ad_id not in favorites.keys():
        favorites.update({ad_id: advertisement})

    history.update({"favorites": favorites})

    with open("history.json", mode="w") as history_file:
        json.dump(history, history_file, indent=4)


def remove_from_favorites(advertisement: dict):
    """Removes an ad from favorites

    :param advertisement: The advertisement to remove from favorites
    :type advertisement: dict"""

    ad_id = advertisement.get("urn").split(":list:")[1]
    with open("history.json", mode="r") as history_file:
        history = json.load(history_file)

    favorites: dict = history.get("favorites")

    if ad_id in favorites.keys():
        favorites.pop(ad_id)

    with open("history.json", mode="w") as history_file:
        json.dump(history, history_file, indent=4)


def purge_pictures():
    """Purges pictures directory"""
    os.system("rm -r pictures")
    os.mkdir("pictures")
    with open("pictures/index.txt", mode="w") as pictures_index:
        pictures_index.write("0")
