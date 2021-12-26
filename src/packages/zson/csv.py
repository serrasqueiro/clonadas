#-*- coding: utf-8 -*-
# csv.py  (c)2021  Henrique Moreira

"""
csv-based table
"""

# pylint: disable=missing-function-docstring

from zson.zobject import ZObject


class CSV(ZObject):
    """ CSV-based table
    """
    _split = ","

    def __init__(self, info=None, encoding="utf-8"):
        """ Initializer: data should be a dictionary or a list.
        """
        self._header_string = ""
        super().__init__(info, encoding)
        assert isinstance(self._table, (list, dict))

    def header(self) -> list:
        """ Returns the header fields, as a list. """
        astr = self._header_string.lstrip("#")
        if not astr:
            return []
        return self._to_row(astr.split(self._split))

    def load(self, path:str, header:str="a") -> bool:
        """ Loads content from file, at 'path'. """
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

    def dump_json(self, key=None) -> str:
        """ Shows dictionary with key,
        or just the header() as key.
        """
        if key is None:
            keystr = self._split.join(self.header())
        else:
            keystr = key
        return self.dumps(self._table, keystr)

    def dump_json_string(self):
        """ Returns the basic json list (string). """
        return self._dump_json_string(self._table)

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
        return [astr.replace("~", self._split) for astr in alist]

    def _from_row(self, alist:list) -> list:
        """ Replaces ',' by '~' """
        if not alist:
            return []
        return [astr.replace(self._split, "~") for astr in alist]

    def _to_csv(self) -> str:
        """ Returns the csv string for the content. """
        astr = self._header_string + "\n"
        return astr + self._csv_payload()

    def _csv_payload(self) -> str:
        astr = ""
        for line in self._table:
            row = self._split.join(self._from_row(line))
            astr += row + "\n"
        return astr

    def __str__(self) -> str:
        return self._csv_payload()

    def __repr__(self) -> str:
        return self.dump_json()


# Main script
if __name__ == "__main__":
    print("Please import me!")
