try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
project_root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(project_root, 'snowclient','VERSION')) as version_file:
    version = version_file.read().strip()

config = {
    'description': 'ServiceNow api client in python',
    'long_description': '''

Python REST client with some extras baked in:

- Request retires built in with appropriated backoffs.
- Wrap response output in object with conviency methods such as being able to resolve depedency tables if they are linked in an attribute ( aka `record.resolve_link("depfield")` ).
- Wrap problems/errors/empty records in NotFound objects.
- Extra querying sugar - see QueryBuilder and docs for details. For example, a request with specific query info like:

GET /api/now/v1/table/change_request?sysparm_limit=10&sysparm_query=cmdb_ciISNOTEMPTY%5Estate=1%5Eassignment_group=deadbeef%5Esys_created_onBETWEENjavascript:gs.dateGenerate('2018-06-11','19:25:00')@javascript:gs.dateGenerate('2018-07-11','19:25:00')%5EORDERBYDESCsys_created_on

Can be generated instead from:

```
qb.field_equals("state", "1")
qb.field_equals("assignment_group", "deadbeef")
start = datetime.utcnow()
end = start - timedelta(days=30)
qb.between(end, start)
qb.orderbydesc("sys_created_on")
```

Which, depending on the eyes (and cough, auto method completions), might hurt just a littttle bit less.

''',
    'author': 'shai rosenfeld',
    'url': 'https://github.com/shaiguitar/snowclient.py',
    'download_url': 'https://github.com/shaiguitar/snowclient.py',
    'author_email': 'shaiguitar@gmail.com',
    'version': version,
    'install_requires': ['nose', 'requests', 'responses', 'backoff'],
    'package_data': {'': ['VERSION','LICENSE.txt']},
    'packages': ['snowclient'],
    'scripts': [],
    'name': 'snowclient'
}

setup(**config)
