# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.


init -1000 python:

    class OrderedDict(dict):
        def __init__(self, *args,**kwargs):
            super().__init__(*args,**kwargs)
            self.keys = list()

        def __setitem__(self, key, value):
            if key not in self:
                self.keys.append(key)
            super(OrderedDict, self).__setitem__(key, value)



        def __delitem__(self, key):
            super(OrderedDict, self).__delitem__(key)
            self.keys.remove(key)

        def append(self,item):
            self[item] = item

        def items(self):
            for key in self.keys:
                yield key, super(OrderedDict, self).__getitem__(key)

        def values(self):
            return [self[key] for key in self.keys]

        def __str__(self):
            return f"OrderedDict|{self.keys}|"

        def __repr__(self):
            return f"OrderedDict|{self.keys}|"

        def pp(self):
            print(f"--- { self} --- ")
            for k,v in self.items():
                print(f"{k}:{v}")