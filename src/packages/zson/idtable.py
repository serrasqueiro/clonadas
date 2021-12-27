#-*- coding: utf-8 -*-
# idtable.py  (c)2021  Henrique Moreira

"""
json-based table
"""

# pylint: disable=missing-function-docstring

import os
import json
from zson.zobject import ZObject
from zson.zindex import ZIndex


class IdTable(ZObject):
    """ JSON-based table
    """
    _table = None
    _index = None

    def __init__(self, info=None, encoding="utf-8"):
        """ Initializer: data should be a dictionary or a list.
        """
        super().__init__(info, encoding)
        assert isinstance(self._table, (list, dict))
        self._index = ZIndex("utf-8")

    def inject(self, obj):
        self._index = ZIndex("utf-8")
        self._table = obj

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
            self._write_content(path, astr)
        except FileNotFoundError:
            return False
        return True

    def dump(self) -> str:
        """ Returns the json equivalent to this table. """
        return self.dumps(self._table)

    def index(self, key:str="data") -> bool:
        """ Tries to index own dictionary. """
        if not isinstance(self._table, dict):
            return False
        data = self._table[key]
        return self._index.do_index(key, data)

    def get_keys(self) -> list:
        """ Returns the list of keys. """
        return sorted(self._index.by_key, key=str.casefold)

    def get_by_key(self, key:str, a_id:int=-1) -> list:
        """ Return list by key. """
        if self._index.by_key is None:
            return []
        if a_id == -1:
            # Returns the list of "Id"(s) key integers:
            return sorted(self._index.by_key[key])
        return self._index.by_key[key][a_id]

    def  _from_data(self, data:str) -> bool:
        """ Read table from data string. """
        inp = json.loads(data)
        self._table = inp
        return True

    def _write_content(self, path:str, astr:str) -> bool:
        if os.name == "nt":
            with open(path, "wb") as fdout:
                fdout.write(astr.encode(self._encoding))
            return True
        with open(path, "w", encoding=self._encoding) as fdout:
            fdout.write(astr)
        return True


# Main script
if __name__ == "__main__":
    print("Please import me!")
