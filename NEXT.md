# Admin on dev:

https://boobooservicecloudopsdev.service-now.com/sys_db_object.do?WSDL

# Have REST explorer access on prod:

https://boobooservicecloudops.service-now.com/nav_to.do?uri=%2F$restapi.do ( nav bar ).

# List of tables:

https://boobooservicecloudopsdev.service-now.com/sys_db_object_list.do?sysparm_userpref_module=7e7ca89ac0a8000901594ba32f405461&sysparm_query=sys_update_nameISNOTEMPTY^EQ&sysparm_clear_stack=true&sysparm_clear_stack=true&sysparm_clear_stack=true

# Service Monikers:

sc_req_item

# list out a graph:

use sysparm_id and tablename as identifiers and then link them via dict
http://www.python-course.eu/graphs_python.php
ie:

a -> b,c
b -> a
c -> e

so get a bunch of resources, start with whatever table, crawl with sysparm_limit 
and make way to other tables and index a graph dict with the (sysparm_id,table_name) as identifiers.
create this graph and display it.

start off with an incident, and graph what connections are related to ONE incident.

# FODE

pyMC at it or tensorflow (more ML/AI analyze graph info).
https://graph-tool.skewed.de/

# Catalog api automation.

See catalog api: https://docs.servicenow.com/bundle/istanbul-servicenow-platform/page/integrate/inbound-rest/concept/c_ServiceCatalogAPI.html
probably should:

- move parsing of is_error (result/error vs http code) crap into the api.py
    have client.py be more focused on things like resolving links, whatever other magic necessary.
    but parsing should be dealt with in api.py

```
########################################################################
{
##   "sys_id": "0006d8ac4fb9be40907685c98310c781",
##   "short_description": "CloudOS App Onboarding (Dev)",
##   "catalogs": [
##     {
##       "sys_id": "e0d08b13c3330100c8b837659bba8fb4",
##       "title": " Cloud Infrastructure and Architecture"
##     }
##   ],
##   "name": "CloudOS App Onboarding",
##   "icon": "images/service_catalog/generic_small.gifx",
##   "description": "<p><font size=\"4\"><strong>Service Description:</strong></font></p>\n<p>Submit this form for Onboarding of applications to CloudOS v2.<br /><br /></p>\n<p><span style=\"font-size: 12pt;\"><strong>What will&nbsp;happen after you have submitted your Request?</strong></span></p>\n<p>The application will be registered in the business service map, access controls will be generated, and CloudOS configuration applied automatically in the <strong>Development environment</strong>.&nbsp;<br /><br /></p>\n<ol>\n<li>User will be notified that the on-boarding process will begin</li>\n<li>AD groups will be created for the specified Moniker.\n<ol style=\"list-style-type: lower-alpha;\">\n<li>Application Admins will be added to the appropriate group</li>\n</ol>\n</li>\n<li>Access to supporting services will given to AD groups.</li>\n<li>CloudOS will be provisioned via automation</li>\n<li>Vault Paths and Mounts will be provisioned via automation</li>\n<li>User will be notified upon process completion with instructions.</li>\n</ol>\n<p>&nbsp;</p>\n<p><span style=\"font-size: 12pt;\"><strong>Who will fulfill my Request?</strong></span></p>\n<ul type=\"disc\">\n<li>Automated&nbsp;</li>\n</ul>\n<p><span style=\"font-size: 12pt;\"><strong>What approvals are required?</strong></span></p>\n<ul type=\"disc\">\n<li>The service owner must approve the request to on-board apps to CloudOS.<br /><br /></li>\n<li>Security and and Cloud Infrastructure approve pull-request during Vault policy&nbsp;creation.<br /><br /></li>\n</ul>\n<p><span style=\"font-size: 12pt;\"><strong>Questions? Comments?</strong></span></p>\n<ul type=\"disc\">\n<li>Please reach out to <a href=\"mailto:cloudos-engg@boobooservice.com\">cloudos-engg@boobooservice.com</a>&nbsp;for CloudOS questions or&nbsp;<a title=\"cloud.ops.portfolio.process.business.tools@boobooservice.com\" href=\"/cloud.ops.portfolio.process.business.tools@boobooservice.com\">cloud.ops.portfolio.process.business.tools@boobooservice.com</a>&nbsp;for form questions.</li>\n</ul>\n<p>&nbsp;</p>",
##   "show_price": false,
##   "type": "catalog_item",
##   "category": {
##     "sys_id": "c5ae8d9ed4fab100537aa3b4f48d9609",
##     "title": "Business Service Management"
##   }
## }
## 
## shai@adsk-lappy ~/r/snowclient.py [forms *] ± % curl 'https://boobooservicecloudopsstg.service-now.com/api/sn_sc/v1/servicecatalog/items' ....
##   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
##                                  Dload  Upload   Total   Spent    Left  Speed
## 100  2565    0  2565    0     0   1325      0 --:--:--  0:00:01 --:--:--  1325
## {
##   "sys_id": "04c0bbc06faa71005b6407321c3ee4f9",
##   "short_description": null,
##   "catalogs": [
##     {
##       "sys_id": "e0d08b13c3330100c8b837659bba8fb4",
##       "title": " Cloud Infrastructure and Architecture"
##     }
##   ],
##   "name": "A360: Cloud Ops SaaS",
##   "icon": "images/nav_bult.gif",
##   "description": "",
##   "show_price": false,
##   "type": "catalog_item",
##   "category": {
##     "sys_id": "81b4bfc06faa71005b6407321c3ee48e",
##     "title": "A360 Projects"
##   }
## }
```
