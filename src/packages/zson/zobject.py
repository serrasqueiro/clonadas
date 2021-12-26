#-*- coding: utf-8 -*-
# zobject.py  (c)2021  Henrique Moreira

"""
json-based table
"""

# pylint: disable=missing-function-docstring, no-self-use

import json


class ZObject():
    """ JSON related operations
    """
    _table = None

    def __init__(self, info, encoding:str):
        self._table = [] if info is None else info
        self._encoding = encoding

    def encoding(self) -> str:
        """ Returns input/ output encoding """
        assert self._encoding
        return self._encoding

    def get(self, as_table=False):
        """ Returns the table content. """
        assert not as_table, "ToDo"
        return self._table

    def dumps(self, data, key:str="data") -> str:
        """ Dumps JSON object """
        content = data if isinstance(data, dict) else self._data_key(data, key)
        astr = self._dump_json_string(content)
        return astr

    def _dump_json_string(self, data) -> str:
        """ Returns JSON string from dictionary or list. """
        astr = json.dumps(data, indent=2, sort_keys=True)
        return astr

    def _data_key(self, obj:list, key:str) -> dict:
        """ Returns dictionary from list """
        isinstance(obj, list)
        return {
            key: obj,
        }


# Main script
if __name__ == "__main__":
    print("Please import me!")
