#-*- coding: utf-8 -*-
# gistsoup.py  (c)2021  Henrique Moreira

"""
Simple converter of tumblr rss into a readable XML for lxml
"""

# pylint: disable=missing-function-docstring, unused-argument

from bs4 import BeautifulSoup


class GistPage():
    """ GistPage -- main purpose is to fetch GIST description within an HTML page
    """
    _candidates = []
    _html, _soup = None, None

    def __init__(self, data:str=""):
        """ Initializer: data should be HTML
        """
        self._html = data
        self._soup = None
        # ...or = open("simple.html", "r", encoding="utf-8").read()
        self._candidates = self._init_candidates(data)


    def gist_description(self, pre="") -> str:
        """ Returns the GIST description string
        """
        #	wget https://gist.github.com/serrasqueiro/4537fea8688ee2712171dd71c5684079
	# or
	#	wget https://gist.github.com/serrasqueiro/4537fea8688ee2712171dd71c5684079 -O out.html
	# Then, read stream and use
	#	lax = yahtml.gistsoup.GistPage(data)
	#	print(lax.gist_description())
        desc = self._candidates
        if not desc:
            return ""
        return pre + "|".join(desc)


    def github_description(self, pre:str="~") -> str:
        """ Returns GITHUB repository description string
        """
        if self._candidates:
            return self.gist_description()
        assert self._soup
        parsed = self._soup
        self._candidates = self._init_github_desc(parsed.find("p"))
        desc = self._candidates
        if not desc:
            return ""
        return pre + "|".join(desc)


    def _init_github_desc(self, items):
        if len(items) != 1:
            return []
        # items.attrs = {'class': ['f4', 'mb-3']}
        candidates = [astr.strip() for astr in items.contents]
        return candidates


    def _init_candidates(self, data:str) -> list:
        """ Returns the candidates of
		<div itemprop="about">
title</div>
        within an HTML string
        """
        parsed = BeautifulSoup(data, features="lxml")
        self._soup = parsed
        if not data:
            return []
        candidates = parsed.find("div", itemprop="about")
        if candidates is None:
            return []
        alpha = [item.strip() for item in candidates.children]
        if not alpha:
            return []
        assert len(alpha) == 1, f"Invalid alpha: {alpha}"
        return alpha


# Main script
if __name__ == "__main__":
    print("Please import me!")
