#-*- coding: utf-8 -*-
# znewdict.py  (c)2022  Henrique Moreira

""" Customized Dictionary

byrder = ("!", "any=", "any-info",)	# ...
new = NewDict(byorder, tbl.get(), name="myname")
"""

# pylint: disable=missing-function-docstring

from zson.zdict import ZDict


class NewDict(ZDict):
    """ Customized dictionary """
    def __init__(self, byorder:tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._byorder = byorder
        self._re_class()

    def items(self) -> list:
        by_key = []
        for substr in self._byorder:
            for key in sorted(self.get_dict()):
                if key.startswith(substr) and key not in by_key:
                    by_key.append(key)
        for key in sorted(self.get_dict()):
            if key not in by_key:
                by_key.append(key)
        return self._items(str, by_key)

    def _re_class(self):
        data = self._data
        cont = {}
        for key, alist in data.items():
            cont[key] = [ZDict(elem) for elem in alist]
        for key in data:
            data[key] = cont[key]


# Main script
if __name__ == "__main__":
    print("Please import me!")
