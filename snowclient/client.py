from snowclient.errors import SnowError

from snowclient.api import Api
from snowclient.snowrecord import SnowRecord

class Client:
    def __init__(self, base_url, username, password):
        self.api = Api(base_url, username, password)

    def list(self,table, **kparams):
        """
        get a collection of records by table name.
        returns a collection of SnowRecord obj.
        """
        result = self.api.list(table, **kparams)
        records = []
        if self.is_error(result):
            msg = result["error"]["message"]
            detail = result["error"]["detail"]
            raise SnowError(msg, detail)
        for elem in result["result"]:
            records.append(SnowRecord(self, table, **elem))
        return records

    def get(self,table, sys_id):
        """
        get a single record by table name and sys_id
        returns a SnowRecord obj.
        """
        result = self.api.get(table, sys_id)
        if self.is_error(result):
            msg = result["error"]["message"]
            detail = result["error"]["detail"]
            raise SnowError(msg, detail)
        return SnowRecord(self, table, **result["result"])

    def resolve_links(self, snow_record):
        """
        Get the infos from the links and return SnowRecords[].
        """
        records = []
        for attr, link in snow_record.links().items():
            records.append(self.resolve_link(snow_record, attr))
        return records

    def resolve_link(self, snow_record, field_to_resolve):
        """
        Get the info from the link and return a SnowRecord.
        """
        link = snow_record.links()[field_to_resolve]

        linked_response = self.api.req("get", link) # rety here...

        rjson = linked_response.json()
        rtablename = SnowRecord.tablename_from_link(link)

        # could do this, but better to not mutate:
        # setattr(snow_record, field_to_resolve, linked)
        #
        # so just return new record. could infer

        if "result" in rjson:
            linked = SnowRecord(self, rtablename, **rjson["result"])
        else:
            linked = SnowRecord.NotFound(self, rtablename, "Could not resolve link %s" % link, [rjson, rtablename, link, self])

        return linked

    def is_error(self, res):
        if "error" in res:
            return True
        elif "result" in res:
            return False
        else:
            raise "parsing the service now responses is hard."

    def is_not_error(self, res):
        return not self.is_error(res)
