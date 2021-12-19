#-*- coding: utf-8 -*-
# gitdescriptions.py  (c)2021  Henrique Moreira

"""
Dumps GIST snippet and GITHUB repos descriptions
"""

# pylint: disable=missing-function-docstring, unused-argument

# requirements.txt
#	BeautifulSoup

import sys
import yahtml.gistsoup


def main():
    """ Main script """
    code = main_run(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""{__file__} command [file ...]

Commands are:
   gist        Show gist description of HTML file
""")
    sys.exit(code if code else 0)


def main_run(out, err, args:list):
    """ Run command """
    code = None
    opts = {}
    if not args:
        return None
    cmd, param = args[0], args[1:]
    if cmd in ("gist",):
        code = dump_gist(param, opts, cmd == "gist")
        return code
    return code


def dump_gist(param, opts, is_gist:bool) -> int:
    encode = "utf-8"
    bugs = 0
    for fname in param:
        what = html_unbone(open(fname, "r", encoding=encode), is_gist)
        desc = what["description"]
        if not desc:
            bugs += 1
            print(f"# Bogus: {fname}")
            continue
        print(f"{fname}: {desc}")
    return 1 if bugs else 0


def html_unbone(data:str, is_gist:bool):
    lax = yahtml.gistsoup.GistPage(data)
    desc = lax.gist_description()
    what = {
        "bones": lax,
        "description": desc,
    }
    return what


# Main script
if __name__ == "__main__":
    main()
