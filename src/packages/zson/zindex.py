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
            if not a_id:
                return False
            adict[a_id] = item
        self.by_key[key] = adict
        return True


# Main script
if __name__ == "__main__":
    print("Please import me!")
