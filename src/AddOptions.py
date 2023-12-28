import inspect
from collections import OrderedDict

class Options:
    def __init__(self, type, method, **kwargs):
        self.type = type
        self.method = method
        self._dict = OrderedDict(kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, *args, **kwargs):
        for arg in args:
            key, _ = self._dict.popitem(last=False)
            setattr(self, key, arg)

        for key, value in kwargs.items():
            if key not in self._dict:
                raise TypeError(f"{key} not an option in {self.type}.{self.method}")
            setattr(self, key, value)

        return self

class AddOptions(type):
    """ A metaclass that takes the dict, and makes it into an option, along with it's name and type """
    def __new__(cls, clsname, bases, attrs, **kwargs):
        updated_attrs = {
            attr: v if attr.startswith("__") else Options(clsname, attr, **v, **kwargs)
            for attr, v in attrs.items()
        }
        # updated_attrs = {}
        # for attr, v in attrs.items():
        #     updated_attrs[attr] = v if attr.startswith("__") else Options(clsname, attr, **v, **kwargs)
        #     if not attr.startswith("__"):
        #         print('-'*50)
        #         print(attr)
        #         print(inspect.getcomments(getattr(globals()[clsname], attr)))

        return super().__new__(cls, clsname, bases, updated_attrs)
