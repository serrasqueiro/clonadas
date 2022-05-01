#-*- coding: utf-8 -*-
# csv.py  (c)2021  Henrique Moreira

"""
csv-based table
"""

# pylint: disable=missing-function-docstring

from zson.zobject import ZObject

ENCODINGS = {
    "latin-1": "ISO-8859-1",
}

TILDE = "~"


class CSV(ZObject):
    """ CSV-based table
    """
    _default_split = ","

    def __init__(self, info=None, encoding="utf-8"):
        """ Initializer: data should be a dictionary or a list.
        """
        self._header_string = ""
        self._split = CSV._default_split
        super().__init__(info, encoding)
        assert isinstance(self._table, (list, dict))

    def header(self) -> list:
        """ Returns the header fields, as a list. """
        astr = self._header_string.lstrip("#")
        if not astr:
            return []
        return self._to_row(astr.split(self._split))

    def convert(self, obj) -> bool:
        """ Converts from another object """
        try:
            cont = obj.get()
        except AttributeError:
            cont = None
        if not cont:
            return self._from_object(obj)
        self._table = cont
        return True

    def load(self, path:str, header:str="a", split_chr=None) -> bool:
        """ Loads content from file, at 'path'. """
        if split_chr is not None:
            self._split = split_chr
        self._table = []
        try:
            with open(path, "r", encoding=self._encoding) as fdin:
                data = fdin.read()
        except FileNotFoundError:
            return False
        return self._from_data(data, header)

    def save(self, path:str) -> bool:
        """ Save content to a file, at 'path'. """
        astr = self._to_csv()
        try:
            with open(path, "w", encoding=self._encoding) as fdout:
                fdout.write(astr)
        except FileNotFoundError:
            return False
        return True

    def dump(self) -> str:
        """ Returns the json equivalent to this table. """
        return self.dumps(self._table)

    def dump_json(self, key=None, key_split=None) -> str:
        """ Shows dictionary with key,
        or just the header() as key.
        """
        achr = self._split if key_split is None else key_split
        if key is None:
            if achr and achr < " ":
                # Assume a semi-colon, instead of a tab (for a better json output!)
                assert achr == "\t", f"Not a tab?, ASCII={ord(achr[0])}d"
                achr = ";"
            keystr = achr.join(self.header())
        else:
            assert isinstance(key, str)
            assert not key_split, "'key_split' only when 'key' is specified"
            keystr = key
        return self.dumps(self._table, keystr)

    def dump_json_string(self):
        """ Returns the basic json list (string). """
        return self._dump_json_string(self._table)

    def rows(self):
        """ Returns the generator object for the table. """
        assert isinstance(self._table, list)
        for row in self._table:
            yield row

    def _from_data(self, data:str, header:str) -> bool:
        """ Read table from data string. """
        this = []
        lines = data.splitlines()
        self._header_string = ""
        assert header in (
            "a",	# automatic
            "n",	# no header
            "1",	# 1-line header
        )
        if not lines:
            return True
        has_head = header == "1" or lines[0].startswith("#")
        if has_head:
            head, tail = lines[0], lines[1:]
        else:
            head, tail = "", lines
        self._header_string = head
        for line in tail:
            this = self._to_row(line.split(self._split))
            self._table.append(this)
        return True

    def _to_row(self, alist:list) -> list:
        """ Replaces '~' by ',' """
        if not alist:
            return []
        return [astr.replace(TILDE, self._split) for astr in alist]

    def _from_row(self, alist:list) -> list:
        """ Replaces ',' by '~' """
        if not alist:
            return []
        return [astr.replace(self._split, TILDE) for astr in alist]

    def _to_csv(self) -> str:
        """ Returns the csv string for the content. """
        astr = self._header_string
        if astr:
            astr += "\n"
        return astr + self._csv_payload()

    def _csv_payload(self) -> str:
        astr = ""
        for line in self._table:
            if isinstance(line, (list, tuple)):
                entry = line
            elif isinstance(line, dict):
                entry = [line[key] for key in sorted(line)]
            else:
                entry = [line]
            row = self._split.join(self._from_row(entry))
            astr += row + "\n"
        return astr

    def _from_object(self, obj) -> bool:
        """ Converts from object. """
        self._header_string = ""
        if isinstance(obj, (list, tuple)):
            self._table = obj
            return True
        if isinstance(obj, str):
            self._header_string = obj
            return True
        return False

    def __str__(self) -> str:
        return self._csv_payload()

    def __repr__(self) -> str:
        return self.dump_json()

    @staticmethod
    def set_separator(split_chr:str=","):
        assert split_chr
        assert isinstance(split_chr, str)
        CSV._default_split = split_chr

    @staticmethod
    def set_tab_separator():
        CSV._default_split = "\t"


# Main script
if __name__ == "__main__":
    print("Please import me!")
