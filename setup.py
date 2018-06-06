try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
project_root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(project_root, 'snowclient','VERSION')) as version_file:
    version = version_file.read().strip()

config = {
    'description': 'snow',
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
