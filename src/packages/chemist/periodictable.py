#-*- coding: utf-8 -*-
# periodictable.py  (c)2021  Henrique Moreira

""" Periodic Table wrapper, reading Excel/ LibreOffice xlsx
"""

# pylint: disable=missing-function-docstring, no-self-use

import xlibre.cell


class WrapText(xlibre.cell.Textual):
    """ Wrapper for xlibre Textual """
    def __init__(self, cell):
        self.string = ""
        super().__init__(cell)
        self.info = self.string
        self.desc = ""

    def description(self) -> str:
        return self.desc


class Reader(dict):
    """ Periodic Table reader
    """
    # pylint: disable=line-too-long

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', '?')
        self._name = name
        dict.__init__(self, *args, **kwargs)
        self._periods = []

    def parse_input(self, rows:list) -> bool:
        def from_period_str(astr:str) -> str:
            if " " in astr:
                return astr.split(" ")[1]
            return astr

        is_ok = False
        for row in rows:
            first, cells = self._process_input_row(row)
            if first or self._periods:
                is_ok = True
                self._periods.append((from_period_str(cells[0].string), cells))
        # Returns True if ok, meaning, at least Hydrogen was seen:
        return is_ok

    def reprocess_table(self) -> list:
        return self._reprocess_table(self.get("table"))

    def _reprocess_table(self, tab):
        if not tab:
            return []
        # The list sometimes has only two elements
        seq = tab.get_key("by-name")
        assert len(seq) >= 2
        last = seq[-1]
        key_list = [elem["Key"] for elem in seq if elem["Key"]]
        parts = {}
        for s_period, elist in self._periods:
            grp_idx = 0
            period = int(s_period)
            parts[period] = {}
            for atom in elist[1:]:
                grp_idx += 1
                key, desc = atom.info, atom.desc
                if not key:
                    continue
                # group is within this iteration
                if key in key_list:
                    continue
                an_id = grp_to_id(grp_idx, period)
                new = {
                    "Id": an_id,
                    "Key": key,
                    "Title": desc,
                    "Trivial": None,
                }
                parts[period][grp_idx] = new
        elems = seq[:-1]
        for grp_idx in range(0, 18+2):
            for period in range(1, 7+1):
                if not parts.get(period):
                    continue
                elem = parts[period].get(grp_idx)
                if not elem:
                    continue
                elems.append(elem)
        elems.append(last)
        return elems

    def _process_input_row(self, row:list) -> tuple:
        # pylint: disable=line-too-long
        """ Relevant row starts with Hydrogen, example:
```
	['Period 1 = "Period 1 element"', 'H = "Hydrogen"', null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 'He = "Helium"']
```
        """
        cells = []
        for acell in row:
            assert acell.string is None or acell.string, f"Invalid cell: {acell.string}"
            new = WrapText(acell.cell())
            astr = better_str(acell.string)     # may be None
            new.string = astr.strip() if astr else astr
            hyl = acell.cell().hyperlink
            if hyl:
                desc = hyl.tooltip
            else:
                desc = None
            new.info = new.string
            if desc:
                new.desc = desc
                new.string += f' = "{desc}"'
            cells.append(new)
        found_one = "Hydrogen" in cells[1].string
        return found_one, cells


def grp_to_id(grp_idx:int, period:int) -> int:
    assert grp_idx >= 1
    gnames = (
        "1a",
        "2",
        "n/a",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
    )
    an_id = 0
    if grp_idx > 1:
        name = gnames[grp_idx - 1]
        if name in ("n/a",):
            an_id = 700
        else:
            an_id = int(name) * 10
    return an_id + period + 1000


def better_str(astr, debug:int=0):
    if astr is None:
        return None
    # n-dash, see       https://unicodemap.org/details/0x2013/
    repl = {
        0xa0: " ",
        0x2013: "-",    # en-dash
    }
    res = ""
    for achr in astr:
        if ' ' <= achr <= '~':
            res += achr
        else:
            new = repl.get(ord(achr))
            if debug > 0 and new is None:
                new = f"({ord(achr)}d=0x{ord(achr):02x})"
            if new:
                res += new
    return res


# Main script
if __name__ == "__main__":
    print("Please import me!")
