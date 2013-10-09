#!/usr/bin/env python3
"""
This example builds on `using_iterator.py` by creating a
function that when called returns a new generator.
"""
import functools
from jama import API, Leaf

api = API()
# Magic numbers will be different for your installation
JAMA_EXAMPLE_NODE_ID, JAMA_EXAMPLE_TYPE = 10552, 87
example_leaf = Leaf(JAMA_EXAMPLE_NODE_ID, JAMA_EXAMPLE_TYPE)


items = functools.partial(api.create_leaf_generator, example_leaf,
                           (
                               "name",
                               "event_code",
                               "event_subcode"
                           )
                         )

items.__doc__ = """
Create a new generator for the Event type.

The returned value can be iterated over directly:
    >>> for event, event_id in items():
    ...     n = event['name']
"""

item_ids = set()
for item, id in items():
    item_ids.add(id)

# We cannot iterate over the same generator a second time
# so we call items again if we needed to.
for item, id in items():
    assert id in item_ids

print("done")