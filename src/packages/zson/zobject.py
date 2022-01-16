#-*- coding: utf-8 -*-
# zobject.py  (c)2021  Henrique Moreira

""" Generic json-based object
"""

# pylint: disable=missing-function-docstring, no-self-use

import json


class ZObject():
    """ JSON related operations
    """
    _table = None
    _do_sort = True
    _msg = ""

    def __init__(self, info, encoding:str):
        assert isinstance(encoding, str)
        self._table = [] if info is None else info
        self._encoding, self._force_ascii = encoding, True
        self._do_sort = True
        self._msg = ""

    def encoding(self) -> str:
        """ Returns input/ output encoding """
        assert self._encoding
        return self._encoding

    def ensure_ascii(self, force_ascii=True):
        self._force_ascii = force_ascii

    def get(self, as_table=False):
        """ Returns the table content. """
        assert not as_table, "ToDo"
        return self._table

    def keying(self, alpha:str="A") -> list:
        """ Return 'A': alphabetical keys (or 'a': case-sensitive sort),
        or 'X'/ 'x': all keys.
        """
        assert isinstance(alpha, str)
        if isinstance(self._table, list):
            assert alpha in "Xx"
            return self._table
        if alpha in "Xx":
            return sorted(self._table, key=str.casefold if alpha == "X" else str)
        if alpha in "Aa":
            alist = sorted(self._table, key=str.casefold if alpha == "X" else str)
            return [astr for astr in alist if astr and astr[0].isalpha()]
        return []

    def get_one(self, name:str):
        """ If name matches exactly one key, returns it.
        If name matches multiple keys, returns None.
        If name does not match anything, returns an empty list.
        """
        _, result = self.get_one_key(name)
        return result

    def get_key(self, name:str):
        """ Returns the table key entry 'name'. """
        if not self._table:
            return None
        return self._table[name]

    def get_one_key(self, name:str) -> tuple:
        """ If name matches exactly one key, returns it.
        If name matches multiple keys, returns None.
        If name does not match anything, returns an empty list.
        """
        res = self._table.get(name)
        key = None
        if res is not None:
            return name, res
        matched = []
        if not isinstance(self._table, dict):
            return None, matched
        for key in self._table:
            if "=" in key and name == key.split("=", maxsplit=1)[0]:
                return key, self._table[key]
            if key.startswith(name):
                matched.append((key, self._table[key]))
        if len(matched) > 1:
            return name, None		# Multiple matches!
        if not matched or key is None:
            return "", []
        return key, matched[0][1]

    def dumps(self, data, key:str="data") -> str:
        """ Dumps JSON object """
        content = data if isinstance(data, dict) else self._data_key(data, key)
        astr = self._dump_json_string(content, self._force_ascii)
        return astr

    def dump_sort(self, sort_keys:bool):
        self._do_sort = sort_keys

    def _dump_json_string(self, data, ensure_ascii=True) -> str:
        """ Returns JSON string from dictionary or list. """
        astr = json.dumps(data, indent=2, sort_keys=self._do_sort, ensure_ascii=ensure_ascii)
        return astr

    def _data_key(self, obj, key:str) -> dict:
        """ Returns dictionary from list """
        if obj is None:
            return { key: None }
        return {
            key: obj,
        }


# Main script
if __name__ == "__main__":
    print("Please import me!")
