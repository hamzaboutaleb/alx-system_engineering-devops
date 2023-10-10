#!/usr/bin/python3
""" task 0 - How many subs"""

import requests


def number_of_subscribers(subreddit):
    """return total subscribers for a given subreddit"""

    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "My-Agent"}
    allow_redirects = False
    response = requests.get(
            url, headers=headers, allow_redirects=allow_redirects)
    if response.status_code == 200:
        try:
            data = response.json()
            subscribers_count = data.get("data").get("subscribers")
            return subscribers_count
        except KeyError:
            return 0
    else:
        return 0
