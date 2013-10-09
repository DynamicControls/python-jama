# Copyright (c) 2013 Dynamic Controls
#
# This program is released under the LGPLv3 License.

import functools
import logging
from suds.client import Client

from jama.version import VERSION
from jama.util import load_config, REQUIRED_KEYS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('jama.api')
logger.setLevel(logging.INFO)


class Connection(object):
    """A proxy for the contour API
    """

    def __init__(self, user, password, url):
        """
        """

        self.client = Client(url)

        # To see all the methods a Client has:
        #print(self.client)

        # create a wsAuth object - your normal username and pass.
        self.auth = self.client.factory.create('ns0:wsAuth')
        self.auth.user = user
        self.auth.password = password


class API(object):

    VERSION = 'v3'  #: Supported jama soap version
    TIMEOUT = 20    #: Timeout in seconds

    def __init__(self, cfg=None):

        # load values from config file
        if cfg is None or isinstance(cfg, (str, unicode)):
            cfg = load_config(cfg)

        for key in REQUIRED_KEYS:
            if getattr(self, key, '???') is None and cfg.get(key, None):
                setattr(self, key, cfg[key])

        logger.debug("Configuration loaded: {}".format(cfg))

        self.conn = Connection(cfg['account'], cfg['password'], cfg['url'])

    def __call__(self, func_name, *args, **kwargs):
        """
        Assume all Jama functions require auth.

        For the Jama Soap: getItem(WsAuth token, java.lang.Long itemId)
            >>> api = API()
            >>> api('getItem', 1234)

        """
        func = getattr(self.conn.client.service, func_name)
        return func(self.conn.auth, *args, **kwargs)

    def create_leaf_generator(self, jama_leaf, interesting_fields):
        """
        Create a generator which yields a tuple (dict, jama_id) for each item
        under a particular leaf.

        :param Leaf jama_leaf:
            The leaf node to iterate over.

        :param iterable interesting_fields:
            Some sequence or mapping of Jama field names that should be returned.
            If a dict is used, the dictionary yielded will use the value from
            interesting_fields as the new key. A mixed approach can be used
            by using a tuple:

            >>> gen = api.create_leaf_generator(parameters_leaf, (("flag1", "Readable Key"), "access_level"))

            The yielded dictionaries contain all "interesting fields" for each item.

        The resulting generator can be iterated over directly:

            >>> for event, jama_id in api.create_leaf_generator(events_leaf, ('name', 'event_code')):
            ...     pass # use event['name']

        Note the second tuple element *jama_id* can be used with other API calls.


        """
        name_map = {k if type(k) == str else k[0]: k if type(k) == str else k[1] for k in interesting_fields}

        def nice_value(field):
            if hasattr(field, "displays"):
                return field.displays[0]
            elif hasattr(field, "values") and field.values:
                return field.values[0]
            else:
                return None

        def is_interesting(field):
            return field.name in name_map

        def item_generator():
            all_items = self.conn.client.service.getChildrenOfItem(self.conn.auth,
                                                                     jama_leaf.document_id,
                                                                     False,
                                                                     0,
                                                                     0)
            logger.debug("Loaded all direct children of item id = {}".format(jama_leaf.document_id))
            for item in all_items:
                logger.debug("Looking at item id = {}".format(item.id))
                if item.documentTypeId != jama_leaf.type_id:
                    logger.debug("Not the droid we're looking for...")
                    continue
                attr = dict([(name_map[f.name], nice_value(f)) for f in item.fields if is_interesting(f)])
                yield attr, item.id

        return item_generator()


class Leaf(object):
    """A proxy for a Jama leaf node

    A particular Jama installation might have often used nodes.
    Leaf objects can be created to access particular types of
    inherited documents from these:

        >>> JAMA_PARAMETER_ID, JAMA_TYPE = 10384, 48
        >>> parameters_leaf = Leaf(JAMA_PARAMETER_ID, JAMA_TYPE)

    """

    def __init__(self, document_id, type_id):
        self.document_id = document_id
        self.type_id = type_id

    def __repr__(self):
        return "<Leaf ID:{}>".format(self.document_id)

    def get_fields(self, connection):
        """
        Return a list of dictionaries where each instance contains
        a label, name, and type of each field.

            >>> parameters_leaf.get_fields(api.conn)

        """
        field_data = connection.client.service.getDocumentTypeFields(connection.auth, self.type_id)
        return [{'label': f.label, 'name': f.name, 'type': f.type} for f in field_data]


if __name__ == "__main__":

    import doctest
    doctest.testmod()
