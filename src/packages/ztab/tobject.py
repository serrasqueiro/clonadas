#-*- coding: utf-8 -*-
# tobject.py  (c)2022  Henrique Moreira

""" Generic json-based object
"""

# pylint: disable=missing-function-docstring

import json

DEFAULT_ENCODING = "ISO-8859-1"

class TObject():
    """ Abstract object: encoding properties and basic JSON capabilities """
    default_encoding = DEFAULT_ENCODING
    _indent_blanks = 2

    """ Generic abstract object. """
    def __init__(self, name:str="", encoding=""):
        self._name = name
        self._obj = []
        self.encoding = encoding if encoding else TObject.default_encoding

    def get_name(self):
        return self._name

    def obj(self):
        """ Returns the (table) object """
        return self._obj

    def _load_json(self, fname:str) -> tuple:
        """ Load json-based text table """
        enc = self.encoding
        with open(fname, "r", encoding=enc) as fdin:
            tbl = json.load(fdin)
        return tbl, True

    def _save_json(self, fname:str, ensure_ascii=True, do_sort=True) -> bool:
        """ Save json-based text table """
        astr = self._dump_json_string(self._obj, do_sort, ensure_ascii)
        assert astr
        enc = "ascii"
        with open(fname, "wb") as fdout:
            fdout.write(astr.encode(enc))
        return True

    def _dump_json_string(self, data, do_sort, ensure_ascii):
        """ Dumps JSON object """
        assert self.encoding, "_dump_json_string()"
        indent = TObject._indent_blanks
        astr = json.dumps(data, indent=indent, sort_keys=do_sort, ensure_ascii=ensure_ascii)
        return astr + "\n"

class DTable(TObject):
    """ Dictionary-based Table """
    def __init__(self, name:str="", encoding=""):
        super().__init__(name, encoding)
        self._format = "LIST"	# ...or DICT

    def reset(self):
        """ Reset data """
        self._obj = []

    def load(self, fname:str) -> bool:
        tbl, is_ok = self._load_json(fname)
        if not is_ok:
            return False
        if isinstance(tbl, dict):
            here = [tbl]
        elif isinstance(tbl, list):
            here = tbl
        else:
            return False
        self._obj = here
        return True

    def save_as_list(self, fname:str) -> bool:
        if isinstance(self._obj, dict):
            return False
        is_ok = self._save_json(fname)
        return is_ok


def ascii_str(astr:str, invalid_chr="") -> str:
    """ Returns a simpler ASCII string
    """
    res = ""
    for achr in astr:
        valid = ' ' <= achr <= '~'
        if not valid:
            new = invalid_chr
        else:
            new = achr
        res += new
    # Could use...	return unidecode.unidecode(astr)
    # but avoiding this import!
    return res


# Main script
if __name__ == "__main__":
    print("Please import me!")
