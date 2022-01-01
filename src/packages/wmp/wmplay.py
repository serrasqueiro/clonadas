#-*- coding: utf-8 -*-
# wmplay.py  (c)2021  Henrique Moreira

""" Win. M. Player
"""

# pylint: disable=missing-function-docstring, no-self-use

import os.path
from os import environ


WMP_LAST_PLAYED = "lastplayed.wpl"


class WMPlay():
    """ Win. M. Player
    """
    _adir = ""

    def __init__(self, where=None):
        if where is None:
            adir = environ.get("LOCALAPPDATA")
            if adir is None:
                adir = ""
            else:
                adir = os.path.join(adir, "Microsoft", "Media Player")
        self._adir = adir
        self._pname = os.path.join(adir, WMP_LAST_PLAYED)

    def last_played(self) -> str:
        """ Returns the path for the "last play" playlist,
        or empty if file not there.
        """
        what = self._pname
        if os.path.isfile(what):
            return what
        return ""



# Main script
if __name__ == "__main__":
    print("Please import me!")
