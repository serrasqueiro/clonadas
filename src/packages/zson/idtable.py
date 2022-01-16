#-*- coding: utf-8 -*-
# idtable.py  (c)2021  Henrique Moreira

"""
json-based table
"""

# pylint: disable=missing-function-docstring, no-self-use

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
        """ Initializer: 'info' should be a dictionary or a list.
        """
        super().__init__(info, encoding)
        assert isinstance(self._table, (list, dict))
        # check_head: whether check data upon input:
        #	n - No check
        #	p - Partial, dictionary
        #	i - Check also 'Id' within
        self.check_head = "n"
        # Indexing:
        self._index = ZIndex("utf-8")

    def inject(self, obj):
        """ Inject a specific table to this instance. """
        self._index = ZIndex("utf-8")
        self._table = obj

    def reset(self, name:str="sample") -> bool:
        """ Generic default IdTable """
        if name.startswith(("!", "~")):
            first = name[1:]
        else:
            first = "!" + name + ".json"
        head = {"Id": 0, "Key": None, "Mark": None, "Title": ""}
        tail = {"Id": -1, "Key": "*", "Title": ""}
        self._table = {
            first: [head],
            "~": [tail],
        }
        return self.index(first)

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

    def _from_data(self, data:str) -> bool:
        """ Read table from data string. """
        inp = json.loads(data)
        self._table = inp
        if self.check_head in "n":
            return True
        self._msg = ""
        msg = self._check_data(data.splitlines())
        self._msg = msg
        if msg:
            return False
        if self.check_head in "i":
            msg = self._check_ids([(key, tbl) for key, tbl in self._table.items()])
        self._msg = msg
        return msg == ""

    def _check_data(self, lines:list) -> str:
        head, tail, payload = lines[0], lines[-1], lines[1:-1]
        is_dict = head == "{"
        if is_dict:
            if tail != "}":
                return "Missing '}'"
        elif head == "[":
            if tail != "]":
                return "Missing ']'"
        else:
            return "Missing {} or []"
        if not is_dict:
            return ""	# assume all ok, simply
        dct, idx = {}, 0
        for line in lines:
            idx += 1
            if not line.startswith('  "'):
                continue
            key = line.split('  "', maxsplit=1)[1].split('"', maxsplit=1)[0]
            if key in dct:
                return f"Line {idx}: Duplicate key '{key}', first found at: {dct[key]}"
            dct[key] = idx
        return ""

    def _check_ids(self, lolist:list) -> str:
        """ Check if 'Id' is unique within all (key, list) """
        for key, alist in lolist:
            if not key:
                continue
            ids = {}
            for elem in alist:
                an_id = elem.get("Id")
                assert an_id is not None, f"Key='{key}', missing 'Id'"
                if an_id in ids:
                    return f"Key='{key}', duplicate Id='{an_id}'"
                ids[an_id] = key
        return ""

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
