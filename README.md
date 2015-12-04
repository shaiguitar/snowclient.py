# Python Api client for Service Now.

Api client for the [docs table api](http://wiki.servicenow.com/index.php?title=Table_API#POST_.2Fapi.2Fnow.2Fv1.2Ftable.2F.28tableName.29&gsc.tab=0).

# Install

```
$ python3.4 setup.py install
# todo soon http://peterdowns.com/posts/first-time-with-pypi.html
```
# Setup

Use something like "~/.snow-auth.json", either way load up basic auth and use `Client()` class
to start hacking away. Or you can just pass it in.
You'll also want/need to use the `QueryBuilder` to abstract away some of
the nastiness of the original syntax necessary. See QueryBuilder tests for it's usage.

# Example

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
    # returns the kind of stuff that you'll never want to write
    # by and that service now likes, such as
    #
    # sysparm_query=sys_created_onBETWEENjavascript:gs.dateGenerate('2013-12-31','00:00:00')@javascript:gs.dateGenerate('2014-01-01','00:00:00')^ORDERBYDESCsys_created_on
```

# Tests

```
# or DEBUG=1 nosetests -s for python requests debugging
# use --nocapture if you want to drop into pdb
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
