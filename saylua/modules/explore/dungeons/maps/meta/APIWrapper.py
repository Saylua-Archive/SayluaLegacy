# APIWrapper -> Required by dungeon(s)
# Syntax sugar.
# ===================================================


class APIWrapper(dict):
    def __init__(self, *args, **kwargs):
        super(APIWrapper, self).__init__(*args, **kwargs)

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

            if kwargs:
                for k, v in kwargs.iteritems():
                    self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)
