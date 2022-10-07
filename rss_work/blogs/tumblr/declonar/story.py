#-*- coding: utf-8 -*-
# story.py  (c)2021  Henrique Moreira

"""
Simple converter of tumblr rss into a readable XML for lxml

see also https://www.jogossantacasa.pt/web/SCRss/rssFeedCartRes -> ISO-8859-1 feed
"""

# pylint: disable=missing-function-docstring, unused-argument

import sys
import os.path
import unidecode
from lxml import etree
from bs4 import BeautifulSoup

#ENCODING_IN = "iso-8859-1"
ENCODING_IN = "utf-8"

def main():
    """ Main script.
    """
    code = run_main(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""story.py [options] STORY-RSS-INPUT

Options are:
   --latin	Use Latin1 (ISO-8859-1) encoding for input.
""")
    sys.exit(code if code else 0)


def run_main(out, err, args):
    """ Main run: returns 0 on success.
    """
    code = run_script(out, err, args)
    return code

def run_script(out, err, args):
    """ Main parsing """
    param = args
    opts = {
        "encoding": ENCODING_IN,
    }
    while param and param[0].startswith("-"):
        if param[0].startswith("--latin"):
            opts["encoding"] = "iso-8859-1"
            del param[0]
            continue
        return None
    if not param:
        return None
    if len(param) > 1:
        return None
    in_file = param[0]
    enc = opts["encoding"]
    msg = handle_rss(out, err, in_file, enc)
    if msg:
        print("Error:", msg)
    return 1 if msg else 0


def handle_rss(out, err, in_file:str, enc:str, postfix:str="_soup") -> str:
    """ Main handler: reads 'in_file.extension' and outputs 'file_soup.extension'
    """
    out_encode = "utf-8"
    assert postfix
    if postfix in in_file:
        err.write("Cannot use file with postfix '{postfix}': {in_file}\n")
        return ""
    extension, alfa = "", in_file.split(".")
    if len(alfa) > 1:
        extension = "." + alfa[-1]
        out_name = '.'.join(alfa[:-1]).rstrip()
    else:
        out_name = in_file
    out_name += postfix + extension
    with open(in_file, "r", encoding=enc) as fdin:
        inputs = fdin.read()
        if inputs.startswith("<?xml version="):
            inputs = inputs[inputs.index("?>") + 2:]
        inputs = inputs.replace("\r", "")
        print("# Head:", "\n".join(inputs.splitlines()[:5]), end="<<<!\n\n")
        astr, root = handle_data(out, inputs)

    # Dump 'root' (XML)
    dump_rss_content(out, root)

    if os.path.isfile(out_name):
        err.write(f"Cowardly refusing to overwrite: {out_name}\n")
        return ""
    with open(out_name, "wb") as fdout:
        fdout.write(astr.encode(out_encode))
    return astr


def handle_data(out, data:str) -> tuple:
    """ Beautifies input with BeautifulSoup
    """
    # see https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    html_doc = data
    soup = BeautifulSoup(html_doc, 'html.parser')
    assert soup
    out_soup = soup.prettify()
    root = etree.fromstring(out_soup)
    return out_soup, root


def dump_rss_content(out, root) -> bool:
    """ Dump XML content to 'out' file """
    channels = [ala for ala in root]
    if not channels:
        return False
    channel = channels[0]
    print(f"# Channels, #{len(channels)}: '{channel.tag}'")
    for child in channel:
        pre = ("-" * 40 + "\n") if child.tag in ("item",) else ""
        out.write(f"{pre}# ::: {child.tag} :::\n")
        for item in child:
            out.write(f"# {item.tag} : {textual(item.text)}\n")
    return True

def textual(astr, as_null="(null)"):
    if astr is None:
        return as_null
    assert isinstance(astr, str)
    new = unidecode.unidecode(astr)
    return new

# Main script
if __name__ == "__main__":
    main()
