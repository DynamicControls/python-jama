#!/usr/bin/env python3
"""
This example references a node id and a document type.
It creates a generator for iterating over said document types
that are direct children of said node.
"""


from jama import API, Leaf

api = API()

# Magic numbers for your installation
JAMA_EXAMPLE_NODE_ID, JAMA_EXAMPLE_TYPE = 10552, 87

example_leaf = Leaf(JAMA_EXAMPLE_NODE_ID, JAMA_EXAMPLE_TYPE)

example_item_generator = api.create_leaf_generator(
    example_leaf,
    ('name',
     ('event_code', 'code')
    ))

for item_dict, jamaid in example_item_generator:
    print(item_dict['name'], item_dict['code'])

