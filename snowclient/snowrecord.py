# http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
# from collections import namedtuple

class SnowRecord:
    def __init__(self, table_name, **entries):
        if table_name is None:
            print("Must provide table name!")
            raise TypeError
        self._table_name = table_name

        # everything else is dynamically set
        # from whatever is returned from the api.
        self.__dict__.update(entries)

    def table_name(self):
        """returns the table_name it was constructed with"""
        # use private variables so to not overwrite
        # any of the data returned back from the api.
        return self._table_name

