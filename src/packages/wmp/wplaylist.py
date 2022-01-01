#-*- coding: utf-8 -*-
# wplaylist.py  (c)2021  Henrique Moreira

""" Win. M. Player playlist
"""

# pylint: disable=missing-function-docstring, no-self-use

from lxml import etree


class Playlist():
    """ Win. M. Player playlist
    """
    _adir = ""
    _resume = None

    def __init__(self, where=None):
        self._resume = None
        if where is None:
            self._root = None
        else:
            self._root = self._from_file(where)

    def get_xml(self):
        assert self._root is not None
        axml = self._root
        self._resume = [
            (idx, [ala.tag for ala in item]) for idx, item in enumerate(axml, start=1)
        ]
        return axml

    def _from_file(self, where:str):
        with open(where, "r", encoding="utf-8") as fdin:
            content = fdin.read()
        root = etree.fromstring(content)
        return root


# Main script
if __name__ == "__main__":
    print("Please import me!")
    #pls = wmp.wplaylist.Playlist(wmp.wmplay.WMPlay().last_played())
