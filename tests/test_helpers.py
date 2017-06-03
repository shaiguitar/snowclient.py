from datetime import *
import ipdb

def to_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

# taken from https://github.com/getsentry/responses/issues/31
# use for responses.activate()
def class_decorating_meta(prefix, *decorators):
    '''
    modified from: http://stackoverflow.com/a/6308016
    '''
    class DecoratingMetaclass(type):
        def __new__(self, class_name, bases, namespace):
            for key, value in list(namespace.items()):
                if not key.startswith(prefix):
                    continue
                if not callable(value):
                    continue
                for decorator in decorators:
                    value = decorator(value)
                namespace[key] = value

            return type.__new__(self, class_name, bases, namespace)

    return DecoratingMetaclass
