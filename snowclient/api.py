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

class Api:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.__username = username
        self.__password = password
        self.logger = logging.getLogger(__name__)

    def list(self,table, **kparams):
        """
        get a collection of records by table name.
        returns a dict (the json map) for python 3.4
        """
        res = self.table_api_get(table, **kparams)
        return res

    def get(self,table, sys_id):
        """
        get a single record by table name and sys_id
        returns a dict (the json map) for python 3.4
        """
        res = self.table_api_get(table, sys_id)
        return res

    #def fatal_code(e):
    #    return 400 <= e.response.status_code < 500

    # backoff/retries built in.
    @backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=8)
                      # giveup=fatal_code)
    def req(self, meth, url):
        """
        sugar that wraps the 'requests' module with basic auth and some headers.
        """
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

    # HELPER, with auth+json/less boilerplate
    def table_api_get(self, *paths, **kparams):
        """
        helper to make GET /api/now/v1/table requests
        """
        url = self.url_for_table_api(*paths, **kparams)
        rjson = self.req("get", url).text

        self.logger.debug("GET json resonse: %s %s" % (url, rjson))

        return json.loads(rjson)

    # HELPER, url builder
    def url_for_table_api(self, *paths, **kparams):
        """
        url builder helper to make /api/now/v1/table paths
        """
        base = self.base_url + "/api/now/v1/table"
        for p in paths:
            base += "/"
            base += p
        if kparams:
            base += "?"
            # use %r in val?
            base += '&'.join("%s=%s" % (key,val) for (key,val) in kparams.items())
        return base
