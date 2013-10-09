#!/usr/bin/env python3

"""
Get a particular item by known ID.
"""

from jama import API

api = API()
item = api('getItem', 1234)
print("Item 1234's description: {}".format(item.description))
