import wget
import json


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

    :param ads: The id of the ad to add to the past_ads_history
    :type ads: str"""

    past_ads = get_past_ads()
    if ad_id not in past_ads:
        past_ads.append(ad_id)

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
