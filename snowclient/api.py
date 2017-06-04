from snowclient.errors import SnowError
from snowclient.snowrecord import SnowRecord
import ipdb
import json
import requests
import backoff
import logging
import os

# LOGGER ... move away from api.
if "DEBUG" in os.environ or "SNOW_DEBUG" in os.environ:
    try:
        # requests pacakge d
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    # this will work only if os.environ is set appropriately...

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


# class Api synonomous with TableApi.
# CatalogApi nested within. (different api)
class Api:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.__username = username
        self.__password = password
        self.logger = logging.getLogger(__name__)
        self.catalog_api = self.CatalogApi(self)

    def list(self,table, **kparams):
        """
        get a collection of records by table name.
        returns a dict (the json map) for python 3.4
        """
        result = self.table_api_get(table, **kparams)
        return self.to_records(result, table)

    def get(self,table, sys_id):
        """
        get a single record by table name and sys_id
        returns a dict (the json map) for python 3.4
        """
        result = self.table_api_get(table, sys_id)
        return self.to_record(result, table)

    # backoff/retries built in.
    # someday? def fatal_code(e): return 400 <= e.response.status_code < 500
    @backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                          max_tries=5)
                      # giveup=fatal_code)
    def req(self, meth, url):
        """
        sugar that wraps the 'requests' module with basic auth and some headers.
        """
        self.logger.debug("Making request: %s %s" % (meth, url))
        req_method = getattr(requests, meth)
        return (req_method(url,
                         auth=(self.__username, self.__password),
                         headers=({'user-agent': self.user_agent(), 'Accept': 'application/json'})))

    def user_agent(self):
        """
        its a user agent string!
        """
        version = ""
        project_root = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(project_root, 'VERSION')) as version_file:
            version = version_file.read().strip()

        return "Python Snow Api Client (Version %s)" % version

    def to_records(self, result, tablename):
        self.raise_if_error(result)

        records = []
        for elem in result["result"]:
            records.append(SnowRecord(self, tablename, **elem))
        return records

    def to_record(self, result, tablename):
        self.raise_if_error(result)

        return SnowRecord(self, tablename, **result["result"])

    def is_error(self, res):
        if "error" in res:
            return True
        elif "result" in res:
            return False
        else:
            raise "parsing the service now responses is hard."

    def is_not_error(self, res):
        return not self.is_error(res)

    def raise_if_error(self, result):
        if self.is_error(result):
            msg = result["error"]["message"]
            detail = result["error"]["detail"]
            raise SnowError(msg, detail)

    def table_api_get(self, *paths, **kparams):
        """ helper to make GET /api/now/v1/table requests """
        url = self.url_for_api("/api/now/v1/table", *paths, **kparams)
        rjson = self.req("get", url).text
        return json.loads(rjson)

    def url_for_api(self, path_prefix, *paths, **kparams):
        """ url builder helper to make /api/now/v1/table paths """

        base = self.base_url + path_prefix
        for p in paths:
            base += "/"
            base += p
        if kparams:
            base += "?"
            # use %r in val?
            base += '&'.join("%s=%s" % (key,val) for (key,val) in kparams.items())
        return base


    # This catalog api is for form/requests etc. catalog api is the interface
    # Wherein folks make requests to modify various table items, take action, etc.
    # This does not fit into the regular flow of the table api.
    # Catalog api docs here:
    #
    # https://docs.servicenow.com/bundle/istanbul-servicenow-platform/page/integrate/inbound-rest/concept/c_ServiceCatalogAPI.html
    #
    class CatalogApi:
        def __init__(self, api):
            self.api = api

        ##### GET #####

        def catalog_get(self, url):
            return json.loads(self.api.req("get", url).text)

        # This method retrieves a list of catalogs to which the user has access.
        def catalogs(self, **kparams):
            url = self.api.url_for_api("/api/sn_sc/v1/servicecatalog/catalogs", **kparams)
            return self.api.to_records(self.catalog_get(url), "SERVICECATALOG:catalog")

        # This method retrieves all the information about a requested catalog.
        def catalog(self, catalog_sys_id):
            url = self.api.url_for_api("/api/sn_sc/v1/servicecatalog/catalogs/%s" % catalog_sys_id)
            return self.api.to_record(self.catalog_get(url), "SERVICECATALOG:catalog")

        # This method retrieves a list of categories for a catalog.
        def categories(self, catalog_sys_id, **kparams):
            url = self.api.url_for_api("/api/sn_sc/servicecatalog/catalogs/%s/categories" % catalog_sys_id, **kparams)
            return self.api.to_records(self.catalog_get(url), "SERVICECATALOG:category")

        # This method retrieves all the information about a requested category.
        def category(self, category_sys_id):
            url = self.api.url_for_api("/api/sn_sc/servicecatalog/categories/%s" % category_sys_id)
            return self.api.to_record(self.catalog_get(url), "SERVICECATALOG:category")

        # This method retrieves a list of catalogs and a list of items for each catalog.
        def items(self, **kparams):
            url = self.api.url_for_api("/api/sn_sc/v1/servicecatalog/items", **kparams)
            return self.api.to_records(self.catalog_get(url), "SERVICECATALOG:item")

        # This method retrieves the catalog item with the specified sys_id.
        def item(self, item_sys_id):
            url = self.api.url_for_api("/api/sn_sc/v1/servicecatalog/items/%s" % item_sys_id)
            return self.api.to_record(self.catalog_get(url), "SERVICECATALOG:item")

        ##### POST #####

        # # This method adds an item to the cart of the current user.
        # def add_to_cart(self, item_sys_id):
        #     url = "/sn_sc/servicecatalog/items/{sys_id}/add_to_cart"
        #     return self.api.to_record(self.catalog_post(url), "SERVICECATALOG:item")



