#-*- coding: utf-8 -*-
# wrap.py  (c)2022  Henrique Moreira

""" Wrapper for common OS operations
"""

# pylint: disable=missing-function-docstring, no-self-use

import os


class Environ():
    """ Environment variables
    """

    def __init__(self):
        self._msg = ""
        self._env = os.environ
        self.update()

    def update(self) -> str:
        """ Updates variables """
        self._env = os.environ
        avar = "USERPROFILE" if os.name == "nt" else "HOME"
        self._home = self.get_var(avar)

    def home(self) -> str:
        """ Returns home variable """
        return self._home

    def vars(self) -> str:
        """ Return environmental vars """
        return self._env

    def get_var(self, name:str="") -> str:
        """ Return environment variable, or empty if does not exist. """
        if not name:
            return ", ".join(sorted(self._env))
        astr = self._env.get(name)
        if astr is None:
            return ""
        return astr

    def var_list(self, prefix:str="") -> list:
        """ Returns the variable list;
        if prefix is not empty, returns the variable list matching the closest string prefix)
        """
        if prefix in self._env:
            return [prefix]
        candidates = {}
        for key in self._env:
            if not key.startswith(prefix):
                continue
            diff = len(key) - len(prefix)
            if diff in candidates:
                item = candidates[diff] + [key]
                candidates[diff] = list(sorted(set(item)))
            else:
                candidates[diff] = [key]
        # Weights linearly: [candidates[item] for item in sorted(candidates)]
        alist = []
        for key in sorted(candidates):
            there = candidates[key]	# this is a list!
            alist.extend(there)
        return alist

    def change_dir(self, path:str="") -> str:
        """ Changes current directory. """
        if path:
            os.chdir(path)
        return os.getcwd()


# Main script
if __name__ == "__main__":
    print("Please import me!")
