#-*- coding: utf-8 -*-
# idtable.py  (c)2021  Henrique Moreira

"""
json-based table
"""

# pylint: disable=missing-function-docstring

import json
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

    def load(self, path:str) -> bool:
        """ Load json content from file. """
        self._table = []
        try:
            with open(path, "r", encoding=self._encoding) as fdin:
                data = fdin.read()
        except FileNotFoundError:
            return False
        return self._from_data(data)

    def save(self, path:str, ensure_ascii=True) -> bool:
        """ Save content to a file, at 'path'. """
        astr = self._dump_json_string(self._table, ensure_ascii=ensure_ascii)
        astr += "\n"
        try:
            with open(path, "w", encoding=self._encoding) as fdout:
                fdout.write(astr)
        except FileNotFoundError:
            return False
        return True

    def dump(self) -> str:
        """ Returns the json equivalent to this table. """
        return self.dumps(self._table)

    def  _from_data(self, data:str) -> bool:
        """ Read table from data string. """
        inp = json.loads(data)
        self._table = inp
        return True


# Main script
if __name__ == "__main__":
    print("Please import me!")
