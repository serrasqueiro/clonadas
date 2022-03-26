#-*- coding: utf-8 -*-
# agit.py  (c)2022  Henrique Moreira

""" Wrapper for common GIT operations

Samles:
	repo = agit.WrapRepo("/mnt/tmp/retokenize", name="mytokens")
	pairs = repo.remote_names()
"""

# pylint: disable=missing-function-docstring

import os
import git
from gitup.wrap import Environ


class GenObject():
    """ Generic Object, abstract class """
    def __init__(self, name:str):
        self._msg = ""
        self.name = name

    def message(self):
        return self._msg


class WrapRepo(GenObject):
    """ Git Repository wrapper
    """
    def __init__(self, path:str="", do_go:bool=True, name=""):
        """ Initializer """
        super().__init__(name)
        self._myenv = Environ()
        self._last = None	# Last operation
        self._repo = None
        if path or do_go:
            self.goto(path)
        self._update_all()

    def is_ok(self) -> bool:
        """ Returns true if repository is there. """
        self._last = None
        if self._repo is None:
            return False
        return os.path.isdir(self._repo.working_dir)

    def repository(self):
        """ Returns the repo -- should be initialized """
        assert self._repo is not None, self.name
        self._update_all()
        return self._repo

    def remotes(self) -> dict:
        """ Return remotes (as a dictionary) """
        return self._remotes

    def remote_names(self) -> list:
        """ Returns the pairs of remote-name and remote-url (alphabetically ordered),
        'origin' will become the first listed if exists.
        """
        basic = ["origin"]
        keylist = list(set(basic + sorted(self._remotes)))
        res = [(key, self._remotes[key]) for key in keylist if key in self._remotes]
        return res

    def clear_last(self, msg:str=""):
        """ Clears last errors stored. """
        self._msg = msg
        self._last = None

    def goto(self, path:str="") -> bool:
        if path:
            self._myenv.change_dir(path)
        self._repo, self._last = None, None
        try:
            self._repo = git.Repo()
        except git.exc.InvalidGitRepositoryError as info:
            self._last = info
            self._msg = str(info)
            return False
        return True

    def branch_list(self) -> list:
        """ Returns the branch listing
        """
        act_branch = self._repo.active_branch.name
        alist = [act_branch]
        return alist

    def _update_all(self):
        self._remote_list, self._remotes = self._update_remotes()

    def _update_remotes(self) -> tuple:
        """ Returns a list of remote triplets, and remotes as a dictionary.
        """
        if self._repo is None:
            return [], {}
        # If there was only one remote:
        #	one = [ala for ala in self._repo.remotes][0]
        # Simpler list:
        #	[(ala.name, ala.url, ala) for ala in self._repo.remotes]
        alist = [(ala.name, ala.url, ala) for ala in self._repo.remotes]
        adict = {}
        for name, url, _ in alist:
            assert name not in adict, f"Duplicate '{name}' ({url})"
            adict[name] = url
        return alist, adict


# Main script
if __name__ == "__main__":
    print("Please import me!")
