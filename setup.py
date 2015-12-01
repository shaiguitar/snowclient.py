try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'snow',
    'author': 'shai rosenfeld',
    'url': 'github',
    'download_url': 'github',
    'author_email': 'shaiguitar@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['snowclient'],
    'scripts': [],
    'name': 'snowclient'
}

setup(**config)
