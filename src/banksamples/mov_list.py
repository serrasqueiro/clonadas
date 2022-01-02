#!/usr/bin/python3
#-*- coding: utf-8 -*-
#
# mov_list.py  (c)2022  Henrique Moreira

""" Dump and update 'mov.lst'
"""
# pylint: disable=missing-function-docstring, unused-argument

import sys
import datetime
from zson.csv import CSV, ENCODINGS


def main():
    """ Main test! """
    code = runner(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""Usage

{__file__} dump|dump-order|update|cat

Commands:
    
dump		Dump mov.lst
dump-order	Dump order of mov.lst
update		Update mov.lst
cat		Dump comprovativo.txu with indexes
""")
    sys.exit(code if code else 0)


def runner(out, err, args):
    """ Wrapper to run. """
    if not args:
        return None
    code = run_dump(out, err, args[0], args[1:])
    return code


def run_dump(out, err, cmd:str, param:list):
    encoding = ENCODINGS["latin-1"]
    f_mov, f_comp = ("mov.lst", "comprovativo.txu")
    if param:
        return None
    acsv = CSV(encoding=encoding)
    comp = CSV(encoding=encoding)
    is_ok = acsv.load(f_mov, split_chr=";")
    if not is_ok:
        err.write(f"Failed reading: {f_mov}\n")
        return 2
    is_ok = comp.load(f_comp, split_chr=";")
    if not is_ok:
        err.write(f"Failed reading: {f_comp}\n")
        return 2
    adict = comprovativo_dict(comp)
    if cmd == "dump":
        is_ok = do_dump(acsv, adict)
        assert is_ok, "Not ordered!"
    elif cmd == "dump-order":
        code = 0 if do_dump(acsv, adict, show="order") else 1
        if code:
            err.write("# Wrong order!\n")
        return code
    elif cmd == "cat":
        do_cat(adict["@by-index"])
    elif cmd == "update":
        msg = do_update(acsv, f_mov, comp, adict)
        if msg:
            err.write(f"No update: {msg}\n")
            return 1
    else:
        return None
    return 0


def do_dump(acsv, acomp, **kwargs) -> bool:
    """ Dump mov.lst in a readable way. """
    ordered = []
    show_kind = kwargs.get("show")
    if show_kind is None:
        show_kind = ""
    assert show_kind in ("", "order"), f"Invalid show='': '{show_kind}'"
    for row in acsv.rows():
        s_key, desc = row
        adate, debt, cred, accsum = s_key.split(",")
        if debt:
            val = -float(debt)
            assert not cred
        else:
            val = float(cred)
            assert not debt
        if show_kind in ("order",):
            print("#", acomp.get(s_key), end=": ")
        print(f"{adate} {val:8.2f} {accsum:>10} {desc}")
        assert s_key in acomp, f"Not found: {s_key}"
        ordered.append(acomp[s_key])
    check = sorted(set(ordered))
    if len(check) != len(ordered):
        print(f"# possible duplicates ({len(check)}, {len(ordered)}):",
              ordered)
        return False
    return check == ordered


def do_cat(byindex:dict):
    """ Dump movements, by line number. """
    for idx in sorted(byindex):
        s_key = byindex[idx]
        print(f"{idx:6} {s_key}")


def comprovativo_dict(comp) -> dict:
    adict = {
        "@by-index": {},
    }
    for idx, row in enumerate(comp.rows(), start=2):
        s_key = comprovativo_row(row)
        adict[s_key] = idx
        adict["@by-index"][idx] = row
    return adict

def comprovativo_row(row:list) -> str:
    pt_date = row[0]
    assert pt_date
    assert len(pt_date) == 10, f"Unrecognized pt date: {pt_date}"
    dttm = datetime.datetime.strptime(pt_date, "%d-%m-%Y")
    iso_date = dttm.strftime("%Y.%m.%d")
    s_key = f"{iso_date},{row[3]},{row[4]},{row[5]}"
    return s_key


def do_update(acsv, f_mov:str, acomp, adict) -> str:
    """ Updates mov.lst, based on keyboard input. """
    lines = []
    byindex = adict["@by-index"]
    assert acomp
    while True:
        keyb = input("enter id and description (or '.' to end) ... ")
        if keyb == ".":
            break
        s_read = keyb.strip()
        if not s_read:
            continue
        tup = s_read.replace("\t", " ").split(" ", maxsplit=1)
        if len(tup) < 2:
            print("Enter number, blank, and description", end="\n\n")
            continue
        s_idx, desc = tup
        idx = int(s_idx)
        desc = desc.strip()
        if idx not in byindex:
            return f"Line {idx} does not exist"
        lines.append((idx, desc, byindex[idx]))
    if not lines:
        return "Nada"
    for idx, desc, info in lines:
        print(idx, desc, f"# {','.join(info)}")
        lst_new = [comprovativo_row(info), desc]
        print(lst_new, end="\n\n")
    for _, desc, info in lines:
        lst_new = [comprovativo_row(info), desc]
        acsv.get().append(lst_new)
    if f_mov:
        acsv.save(f_mov)
    else:
        print(":::\n" + str(acsv), end="<<<\n")
    return ""


# Main script
if __name__ == "__main__":
    main()
