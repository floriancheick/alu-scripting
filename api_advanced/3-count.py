#!/usr/bin/python3
""" Module"""
import requests


def count_words(subreddit, word_list, word_count=[], after=None):
"""Module"""

    word_list = [word.lower() for word in word_list]

    if bool(word_count) is False:
        for word in word_list:
            word_count.append(0)

    url = 'https://www.reddit.com/r/{}/hot.json?after={}'.format(subreddit,
                                                                 after)
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})

    res = requests.get(url, headers=headers, allow_redirects=False)
    if res.status_code == 200:
        req = res.json()
        for child in req['data']['children']:
            i = 0
            for i in range(len(word_list)):
                for name in [word for word in child['data']['title'].split()]:
                    name = name.lower()
                    if word_list[i] == name:
                        word_count[i] += 1
                i += 1
        if req['data']['after'] is not None:
            count_words(subreddit, word_list,
                        word_count, req['data']['after'])

        else:
            nary = {}
            for key_word in list(set(word_list)):
                i = word_list.index(key_word)

                if word_count[i] != 0:
                    nary[word_list[i]] = (word_count[i] *
                                          word_list.count(word_list[i]))

            for key, val in sorted(nary.items(), key=lambda x: (-x[1], x[0])):
                if val:
                    print('{}: {}'.format(key, val))
