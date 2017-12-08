# Python Api client for Service Now.

Api client for the [docs table api](http://wiki.servicenow.com/index.php?title=Table_API#POST_.2Fapi.2Fnow.2Fv1.2Ftable.2F.28tableName.29&gsc.tab=0).

# Usage

See an [example](docs/ex1.py) in the docs dir. tl;dr -

```python
  # re-tailor for your own uses (tablename here is 'incident', base url, auth, etc)
  client = Client("https://your-sandbox.service-now.com", user, password)
  recent_incidents = client.list("incident", sysparm_limit=1000, sysparm_query=build_query())
  i = recent_incidents[0]
  i.u_custom_field # returns custom value
```

You'll probably want to use the querybuilder to avoid having to do this yourself.

```
def build_query():
    qb = QueryBuilder()
    qb.between(start, end)
    qb.orderbydesc("sys_created_on")
    return qb.return_query
    #
    # there are more things available:
    # qb.field_equals("bar", "baz")
    # see more examples at test cases


    # 
    # returns the kind of stuff that you'll never want to write
    # by and that service now likes, such as
    #
    # sysparm_query=sys_created_onBETWEENjavascript:gs.dateGenerate('2013-12-31','00:00:00')@javascript:gs.dateGenerate('2014-01-01','00:00:00')^ORDERBYDESCsys_created_on
```


# Install

```
shai@adsk-lappy ~   % pip3.4 install snowclient
Collecting snowclient
  Downloading snowclient-0.3.1.tar.gz
  ...
  ...
  Running setup.py install for snowclient
Successfully installed snowclient-0.3.1
```

# Releasing

Per http://peterdowns.com/posts/first-time-with-pypi.html (depends on `~/.pypirc` file).

It's at https://pypi.python.org/pypi?:action=display&name=snowclient&version=0.3.1

# Setup

Use something like "~/.snow-auth.json", either way load up basic auth and use `Client()` class
to start hacking away. Or you can just pass it in.
You'll also want/need to use the `QueryBuilder` to abstract away some of
the nastiness of the original syntax necessary. See QueryBuilder tests for it's usage.

# Tests

```
# or DEBUG=1 nosetests -s for python requests debugging
# use --nocapture if you want to drop into pdb
# or for more verbose nosetests -vvs tests/
# ultimately though:
$ nosetests
.
----------------------------
Ran 1 test in 0.003s
```

# WIP

I'm using it, but consider it WIP. I built only the parts of the api I needed so this is not complete.

It will be over time if it gets the TLC it needs. Contributions very welcome of course. 

Hope you find it helpful!

# Api docs

Other docs:

- [legacy api docs](http://wiki.servicenow.com/index.php?title=Legacy:JSON_Web_Service#gsc.tab=0)
- [docs table api](http://wiki.servicenow.com/index.php?title=Table_API#POST_.2Fapi.2Fnow.2Fv1.2Ftable.2F.28tableName.29&gsc.tab=0)
- [docs rest api](http://wiki.servicenow.com/index.php?title=REST_API#Security&gsc.tab=0)
- [midserver](https://docs.servicenow.com/bundle/helsinki-it-operations-management/page/product/mid-server/concept/c_MIDServerArchitecture.html)
