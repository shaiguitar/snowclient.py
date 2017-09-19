from datetime import *


class QueryBuilder:
# snow query helper - help generate the crazy stuff service now expects
# whether it be dates, orderby, etc.

    # NB: http://wiki.servicenow.com/index.php?title=Operators_Available_for_Filters_and_Queries#gsc.tab=0
    # lot of things to extend this query builder with.

    def __init__(self):
        # maintain state so these methods are chainable.
        self.return_query = ""
        self._append_method = "AND"

    def orderby(self, field):
        self._append("ORDERBY{0}".format(field))
        return self

    def orderbydesc(self, field):
        self._append("ORDERBYDESC{0}".format(field))
        return self

    def field_equals(self, field, value):
        self._append("{0}={1}".format(field, value))
        return self

    def field_empty(self, field):
        self._append("{0}ISEMPTY".format(field))
        return self

    def field_empty_string(self, field):
        self._append("{0}EMPTYSTRING".format(field))
        return self

    def field_not_empty(self, field):
        self._append("{0}ISNOTEMPTY".format(field))
        return self

    # sys_created_onBETWEENjavascript:gs.dateGenerate('2015-04-16','00:10:00')@javascript:gs.dateGenerate('2015-04-22','12:59:59')
    def between(self, start, end, field='sys_created_on'):
        s = self._comma_snow_date(start)
        e = self._comma_snow_date(end)
        self._append(field + "BETWEEN" + "javascript:gs.dateGenerate({0})@javascript:gs.dateGenerate({1})".format(s,e))
        return self

    def gt(self, start):
        return false
        # impelment
        # return self

    def lt(self, start):
        return false
        # implement
        # return self

    def OR(self):
        self._append_method = "OR"
        return self

    def _append(self, str):
        # how service now wants it ("and") - with a carat.
        # http://wiki.servicenow.com/index.php?title=Encoded_Query_Strings#Using_Multiple_Conditions
        if self.return_query == "":
          self.return_query += str
          return

        if self.return_query != "":
            if self._append_method == "AND":
                self.return_query += "^"
            elif self._append_method == "OR":
                self.return_query += "^OR"
                self._append_method = "AND" # reset it, just use once.
            else:
                raise ValueError
        self.return_query += str

    def _comma_snow_date(self, date):
        return date.strftime("'%Y-%m-%d','%H:%M:%S'")

