#-*- coding: utf-8 -*-
# use_agit.py  (c)2022  Henrique Moreira

""" Sample for using 'agit'
"""

# pylint: disable=missing-function-docstring

import sys
from gitup.agit import WrapRepo

def main():
    run_test(sys.argv[1:])

def run_test(args):
    """ Main run! """
    param = []
    if args:
        param = args
        adir = param[0]
        del param[0]
    else:
        adir = ""
    assert not param, f"Too many params: {param}"
    is_ok = run_wrap(adir)
    if not is_ok:
        print("Uops!", adir)
    return is_ok

def run_wrap(param:str) -> bool:
    rref = WrapRepo(param)
    if not rref.is_ok():
        return False
    is_ok = go_checkout_pull(rref, "master")
    return is_ok

def go_checkout_pull(rref, master):
    repo = rref.repository()
    print("BRANCH LIST:", rref.branch_list())
    ori = rref.repository().remotes.origin
    if master not in rref.branch_list():
        print("'master' branch is not part of the branch list!")
    repo.create_head(master, ori.refs.master).set_tracking_branch(ori.refs.master).checkout()
    xyz = repo.heads[master]
    assert repo.heads.master == xyz
    branches = rref.branch_list()
    print("# Branches:", branches)
    # Checking out master
    assert master in branches, f"'master' not found in branches: {branches}"
    print("Pulling from remote...", rref.remote_names(), end="\n\n")
    res = ori.pull()
    print("Pulling tags...")
    ori.pull("--tags")
    print("Pushing...", master)
    ori.push()
    assert res
    print("PULL CODES:", [ala.flags for ala in res])
    print(res)
    return True

if __name__ == "__main__":
    main()
