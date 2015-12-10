class SnowError(Exception):
    def __init__(self, msg, detail=None):
        self.msg = msg
        self.detail = detail

    def __str__(self):
        return repr(self.msg)
