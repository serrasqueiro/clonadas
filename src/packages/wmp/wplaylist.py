#-*- coding: utf-8 -*-
# wplaylist.py  (c)2021  Henrique Moreira

""" Win. M. Player playlist
"""

# pylint: disable=missing-function-docstring, no-self-use

from lxml import etree


class Playlist(dict):
    """ Win. M. Player playlist
    """
    _adir = ""
    _resume = None

    def __init__(self, where=None, **kwargs):
        dict.__init__(self, **kwargs)
        self._resume = None
        if where is None:
            self._root = None
        else:
            self._root = self._from_file(where)

    def parse(self) -> bool:
        self.get_xml()
        return len(self["seq"]) > 0

    def media_list(self) -> list:
        """ Returns list of paths. """
        if "media" not in self:
            self.parse()
        res = [attr["src"] for _, attr, _ in self["media"]]
        return res

    def get_xml(self):
        assert self._root is not None
        axml = self._root
        self._resume = [
            (idx, [ala.tag for ala in item]) for idx, item in enumerate(axml, start=1)
        ]
        seqs = [item for item in axml.findall(".*/seq")]
        self["seq"] = seqs
        self["media"] = self._from_seq(seqs[0]) if len(seqs) == 1 else []
        return axml

    def _from_file(self, where:str):
        with open(where, "r", encoding="utf-8") as fdin:
            content = fdin.read()
        root = etree.fromstring(content)
        return root

    def _from_seq(self, one) -> list:
        """ Returns a list of triplets:
		1. idx (1..n)
		2. attributes
		3. (raw) item - xml 'Element'
        """
        media = [
            (idx, item.attrib, item) for idx, item in enumerate(one, start=1) if item.tag == "media"
        ]
        return media


# Main script
if __name__ == "__main__":
    print("Please import me!")
    #pls = wmp.wplaylist.Playlist(wmp.wmplay.WMPlay().last_played())
