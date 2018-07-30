from snowclient.errors import SnowError
from snowclient.snowrecord import SnowRecord

from snowclient.api import Api

class Client:
    def __init__(self, base_url, username, password):
        self.api = Api(base_url, username, password)

    def list(self,table, **kparams):
        """
        get a collection of records by table name.
        returns a collection of SnowRecord obj.
        """
        records = self.api.list(table, **kparams)
        return records

    def get(self,table, sys_id):
        """
        get a single record by table name and sys_id
        returns a SnowRecord obj.
        """
        record = self.api.get(table, sys_id)
        return record

    def update(self,table, sys_id, **kparams):
        """
        update a record via table api, kparams being the dict of PUT params to update.
        returns a SnowRecord obj.
        """
        record = self.api.update(table, sys_id, **kparams)
        return record

