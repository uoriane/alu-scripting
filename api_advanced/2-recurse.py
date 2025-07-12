#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns a list of titles
of all hot articles for a given subreddit. Returns None if subreddit is invalid.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Returns a list of titles of all hot articles for a given subreddit"""
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'MyRedditScraper/1.0'
    }
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        res = requests.get(
            url, headers=headers, params=params, allow_redirects=False)
        if res.status_code != 200:
            return None

        data = res.json().get('data', {})
        children = data.get('children', [])
        for child in children:
            hot_list.append(child.get('data', {}).get('title'))

        next_after = data.get('after')
        if next_after:
            return recurse(subreddit, hot_list, next_after)

        return hot_list

    except Exception:
        return None

