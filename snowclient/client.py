import json
import requests
import logging
import os

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
        for elem in result['result']:
            records.append(SnowRecord(table, **elem))
        return records

    def get(self,table, sys_id):
        """
        get a single record by table name and sys_id
        returns a SnowRecord obj.
        """
        result = self.api.get(table, sys_id)
        return SnowRecord(table, **result['result'])

    def resolve_links(self, snow_record):
        """
        Finds any dict values that have 'link' in them, and assoc the new thing in as a replacement
        for the original <link> value. The replacement is a SnowRecord
        """
        replace_dict = {}
        for key, value in snow_record.__dict__.items():
            if isinstance(value, dict) and value['link']:
                # sys_id = value['value']
                link = value['link']
                linked_response = self.api.req("get", link)
                replace_dict[key] = {"json": linked_response.json(),
                                     "tablename": self.tablename_from_link(link) }
        for key, value in replace_dict.items():
            if replace_dict[key]:
                data = {}
                if "result" in replace_dict[key]["json"]:
                    data = replace_dict[key]["json"]["result"]
                else:
                    # raise BAD RESPONSE (?)
                    data = replace_dict[key]["json"]
                setattr(snow_record, key, SnowRecord(replace_dict[key]["tablename"], **data))
        return snow_record

    def tablename_from_link(self, link):
        """
        Helper method for URL's that look like /api/now/v1/table/FOO/sys_id etc.
        """
        arr = link.split("/")
        i = arr.index("table")
        tn = arr[i+1]
        return tn
