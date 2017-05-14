# http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
# from collections import namedtuple would be good, but the objects are built
# dynamically from the response. there is no set idea of what the fields are.

import ipdb

class SnowRecord:
    def tablename_from_link(link):
        """
        Helper method for URL's that look like /api/now/v1/table/FOO/sys_id etc.
        """
        arr = link.split("/")
        i = arr.index("table")
        tn = arr[i+1]
        return tn

    def __init__(self, client, table_name, **entries):
        self._client = client

        if table_name is None:
            print("Must provide table name!")
            raise TypeError
        self._table_name = table_name

        self._attrs = []
        for key in entries:
            self._attrs.append(key)

        # everything else is dynamically set
        # from whatever is returned from the api.
        self.__dict__.update(entries)

    def resolve_links(self):
        """
        a sugar method (could be called from client) to resolve dependencies of this object.
        """
        return self._client.resolve_links(self)

    def resolve_link(self, field_to_resolve):
        """
        a sugar method (could be called from client) to resolve field of this object.
        """
        return self._client.resolve_link(self, field_to_resolve)

    def identtuple(self):
        """ identity for graph node/vertex purposes """
        return (self._table_name, self.sys_id)

    def links(self):
        """
        returns {attr1: href, attr2: href2}
        """
        dlinks = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict) and value['link']:
                dlinks[key] = value['link']
        return dlinks

    # this might be nice but not ipmortant at this time.
    # ie, subscriptable access snow_record['attr']
    #
    # def __getitem__(self, k):
    #    getattr(self, k)

    class NotFound:
        def __init__(self, client, table_name, msg, data):
            self._client = client
            self._table_name = table_name
            self.msg  = msg
            self.data = data

        def identtuple(self):
            """ identity for graph node/vertex purposes """
            s = ','.join(str(x) for x in self.data)
            return (self._table_name, s)

