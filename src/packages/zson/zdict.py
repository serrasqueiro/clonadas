#-*- coding: utf-8 -*-
# zdict.py  (c)2021  Henrique Moreira

"""
dictionary based class(es)

Examples:
  obj = zson.zdict.ZDict({"planets": ["venus", "earth"], "animal": ["pig", "dog"]})
"""

# pylint: disable=missing-function-docstring, no-self-use


class ZDict(dict):
    """ Dictionary related operations
    """
    _name = ""
    _data = None

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', '')
        self._name = name
        assert len(args) == 1, f"Unexpected args ({name}): {len(args)}"
        dict.__init__(self, *args, **kwargs)
        self._data = args[0]

    def get_name(self) -> str:
        return self._name

    def get_dict(self) -> dict:
        return self._data

    def _items(self, order, keying=None) -> list:
        """ Returns items from a dictionary-like var """
        res = []
        data = self._data
        if keying:
            by_key = keying
        else:
            by_key = sorted(data, key=order)
        for key in by_key:
            res.append((key, data[key]))
        return res

    def items(self) -> list:
        return self._items(order=str.casefold)

    #def default(self, obj):
    #    iterable = iter(obj)
    #    return list(iterable)

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self):
        return repr(self._data)


# Main script
if __name__ == "__main__":
    print("Please import me!")
