from functools import wraps


def lazy_loader(func):
    @wraps(func)
    def execute(self, *args, **kwargs):
        if self.logger is None:
            self.init()
        return func(self, *args, **kwargs)

    return execute
