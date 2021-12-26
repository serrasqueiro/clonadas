#-*- coding: utf-8 -*-
# idtable.py  (c)2021  Henrique Moreira

"""
json-based table
"""

# pylint: disable=missing-function-docstring

from zson.zobject import ZObject


class IdTable(ZObject):
    """ JSON-based table
    """
    _table = None

    def __init__(self, info=None, encoding="utf-8"):
        """ Initializer: data should be a dictionary or a list.
        """
        super().__init__(info, encoding)
        assert isinstance(self._table, (list, dict))

    def dump(self) -> str:
        """ Returns the json equivalent to this table. """
        return self.dumps(self._table)


# Main script
if __name__ == "__main__":
    print("Please import me!")
