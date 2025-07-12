#!/usr/bin/python3
"""Recursive function that returns all hot article titles from a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Returns a list of titles of all hot articles for a given subreddit.
    If subreddit is invalid, returns None.
    """
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'python:subreddit.hot:v1.0 (by /u/yourusername)'
    }
    params = {'limit': 100}
    if after:
        params['after'] = after

    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)

    # If invalid subreddit or other failure
    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    posts = data.get("children", [])

    for post in posts:
        title = post.get("data", {}).get("title")
        if title:
            hot_list.append(title)

    next_after = data.get("after")
    if next_after:
        return recurse(subreddit, hot_list, next_after)

    return hot_list


