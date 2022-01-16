#-*- coding: utf-8 -*-
# zindex.py  (c)2021  Henrique Moreira

""" Standard indexing based on "Id"(s), for json tables
"""

# pylint: disable=missing-function-docstring, no-self-use

from zson.zobject import ZObject

KEY_ID_STR = "Id"


class ZIndex(ZObject):
    """ Indexing
    """
    by_key = None

    def __init__(self, encoding:str):
        super().__init__({"index": []}, encoding)
        self.by_key = {}

    def do_index(self, key:str, data) -> bool:
        self.by_key[key] = {}
        if not isinstance(data, list):
            return False
        adict = {}
        for item in data:
            a_id = item.get(KEY_ID_STR)
            if a_id < -1:
                return False
            adict[a_id] = item
        self.by_key[key] = adict
        return True


class DataSeq(ZObject):
    """ Simple sorting (of tables) """
    def __init__(self, info, encoding:str="ascii"):
        super().__init__({"index": [], "data": info}, encoding)
        self.by_key = {}

    def do_index(self, by_key_idx=None) -> bool:
        key_idxs = [0] if by_key_idx is None else by_key_idx
        assert isinstance(key_idxs, (list, tuple))
        data = self._table["data"]
        seq = []
        self._table["order"] = seq
        if len(key_idxs) <= 0:
            return False
        first = key_idxs[0]
        if len(key_idxs) == 1:
            seq = sorted(data, key=lambda x: x[first])
        else:
            seq = sorted(data, key=lambda x: lambda_key_idxs(key_idxs, x))
        self._table["order"] = seq
        return True

    def get_order(self) -> list:
        """ Returns items as ordered (by do_index()) """
        return self._table["order"] if "order" in self._table else []


def lambda_key_idxs(key_idxs:list, tup, none_is:str=""):
    """ Lambda function for keying of a list ('tup') """

    def stringify(ala):
        if ala is None:
            return none_is
        if isinstance(ala, (int, float)):
            value = float(ala)
            return f"{value:20.9f}"
        return str(ala)

    keys = key_idxs
    items = [stringify(tup[idx]) for idx in keys]
    return '+'.join(items)

# Main script
if __name__ == "__main__":
    print("Please import me!")
