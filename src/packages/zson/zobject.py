#-*- coding: utf-8 -*-
# zobject.py  (c)2021, 2022  Henrique Moreira

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

    def message(self):
        """ Returns the (error) message """
        return self._msg

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

    def get_one_key(self, name:str, function=None) -> tuple:
        """ If name matches exactly one key, returns it.
        If name matches multiple keys, returns None.
        If name does not match anything, returns an empty list.
        """
        name_compare = default_name_compare if function is None else function
        res = self._table.get(name)
        key, found_key = None, None
        if res is not None:
            return name, res
        matched = []
        if not isinstance(self._table, dict):
            return None, matched
        for key in self._table:
            if "=" in key and name == key.split("=", maxsplit=1)[0]:
                return key, self._table[key]
            if name_compare(key, name):
                found_key = key
                matched.append((key, self._table[key]))
        if len(matched) > 1:
            return name, None		# Multiple matches!
        if found_key is None:
            return "", []
        #print("# found single match:", matched[0])
        return found_key, matched[0][1]

    def get_key_hint(self, name:str) -> tuple:
        """ Returns triplet, instead of pair (get_one_key).
		1. the complete table string
		2. the content of the table
		3. the hint associated with TABLE=<EXPR>
        """
        key, matched = self.get_one_key(name)
        if key and matched and key in self._table:
            hint = key.split("=", maxsplit=1)[-1]
            return key, matched, hint
        return key, matched, None

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

    def key_names_diff(self, key1, key2) -> tuple:
        """ Returns an empty tuple if key list 1 and key list 2 match.
        Also allows key dictionaries.
        If key1 != key2, a tuple with all differences is returned.
        """
        diffs = []
        if isinstance(key1, dict):
            return self.key_names_diff(sorted(key1), sorted(key2))
        #print(":::", key1, "vs", key2)
        for key in sorted(key1):
            if key not in key2:
                diffs.append(f"+{key}")
        for key in sorted(key2):
            if key not in key1:
                diffs.append(f"-{key}")
        return tuple(diffs)

    def _data_key(self, obj, key:str) -> dict:
        """ Returns dictionary from list """
        if obj is None:
            return { key: None }
        return {
            key: obj,
        }


def default_name_compare(key:str, name:str) -> int:
    """ Default name compare is startswith: returns 1 if True, 2 if exact match.
    """
    assert isinstance(key, str)
    if key == name:
        return 2
    return int(key.startswith(name))


# Main script
if __name__ == "__main__":
    print("Please import me!")
