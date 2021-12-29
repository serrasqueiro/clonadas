#-*- coding: utf-8 -*-
# atoms.py  (c)2021  Henrique Moreira

""" Periodic Table wrapper, reading Excel/ LibreOffice xlsx

Examples:
	tbl = zson.idtable.IdTable(); tbl.load("sample.json")
	atoms = chemist.atoms.Elements(tbl.get_key("by-name"))
        print(toms.by_id()[atoms.named("Cs")["Id"]].props)
		{'Id': 1006, 'Key': 'Cs', 'Title': 'Caesium', 'Trivial': None, 'Weight': 55, 'Wsa': '132.91'}

"""

# pylint: disable=missing-function-docstring, no-self-use

ATOMS = {
    "H":	("Hydro-gen", "1.008"),
    "He":	("He-lium", "4.0026"),
    "Li":	("Lith-ium", "6.94"),
    "Be":	("Beryl-lium", "9.0122"),
    "B":	("Boron", "10.81"),
    "C":	("Carbon", "12.011"),
    "N":	("Nitro-gen", "14.007"),
    "O":	("Oxy-gen", "15.999"),
    "F":	("Fluor-ine", "18.998"),
    "Ne":	("Neon", "20.180"),
    "Na":	("So-dium", "22.990"),
    "Mg":	("Magne-sium", "24.305"),
    "Al":	("Alumin-ium", "26.982"),
    "Si":	("Sili-con", "28.085"),
    "P":	("Phos-phorus", "30.974"),
    "S":	("Sulfur", "32.06"),
    "Cl":	("Chlor-ine", "35.45"),
    "Ar":	("Argon", "39.95"),
    "K":	("Potas-sium", "39.098"),
    "Ca":	("Cal-cium", "40.078"),
    "Sc":	("Scan-dium", "44.956"),
    "Ti":	("Tita-nium", "47.867"),
    "V":	("Vana-dium", "50.942"),
    "Cr":	("Chrom-ium", "51.996"),
    "Mn":	("Manga-nese", "54.938"),
    "Fe":	("Iron", "55.845"),
    "Co":	("Cobalt", "58.933"),
    "Ni":	("Nickel", "58.693"),
    "Cu":	("Copper", "63.546"),
    "Zn":	("Zinc", "65.38"),
    "Ga":	("Gallium", "69.723"),
    "Ge":	("Germa-nium", "72.630"),
    "As":	("Arsenic", "74.922"),
    "Se":	("Sele-nium", "78.971"),
    "Br":	("Bromine", "79.904"),
    "Kr":	("Kryp-ton", "83.798"),
    "Rb":	("Rubid-ium", "85.468"),
    "Sr":	("Stront-ium", "87.62"),
    "Y":	("Yttrium", "88.906"),
    "Zr":	("Zirco-nium", "91.224"),
    "Nb":	("Nio-bium", "92.906"),
    "Mo":	("Molyb-denum", "95.95"),
    "Tc":	("Tech-netium", "[97]"),
    "Ru":	("Ruthe-nium", "101.07"),
    "Rh":	("Rho-dium", "102.91"),
    "Pd":	("Pallad-ium", "106.42"),
    "Ag":	("Silver", "107.87"),
    "Cd":	("Cad-mium", "112.41"),
    "In":	("Indium", "114.82"),
    "Sn":	("Tin", "118.71"),
    "Sb":	("Anti-mony", "121.76"),
    "Te":	("Tellur-ium", "127.60"),
    "I":	("Iodine", "126.90"),
    "Xe":	("Xenon", "131.29"),
    "Cs":	("Cae-sium", "132.91"),
    "Ba":	("Ba-rium", "137.33"),
    "Lu":	("Lute-tium", "174.97"),
    "Hf":	("Haf-nium", "178.49"),
    "Ta":	("Tanta-lum", "180.95"),
    "W":	("Tung-sten", "183.84"),
    "Re":	("Rhe-nium", "186.21"),
    "Os":	("Os-mium", "190.23"),
    "Ir":	("Iridium", "192.22"),
    "Pt":	("Plat-inum", "195.08"),
    "Au":	("Gold", "196.97"),
    "Hg":	("Mer-cury", "200.59"),
    "Tl":	("Thallium", "204.38"),
    "Pb":	("Lead", "207.2"),
    "Bi":	("Bis-muth", "208.98"),
    "Po":	("Polo-nium", "[209]"),
    "At":	("Asta-tine", "[210]"),
    "Rn":	("Radon", "[222]"),
    "Fr":	("Fran-cium", "[223]"),
    "Ra":	("Ra-dium", "[226]"),
    "Lr":	("Lawren-cium", "[266]"),
    "Rf":	("Ruther-fordium", "[267]"),
    "Db":	("Dub-nium", "[268]"),
    "Sg":	("Sea-borgium", "[269]"),
    "Bh":	("Bohr-ium", "[270]"),
    "Hs":	("Has-sium", "[269]"),
    "Mt":	("Meit-nerium", "[278]"),
    "Ds":	("Darm-stadtium", "[281]"),
    "Rg":	("Roent-genium", "[282]"),
    "Cn":	("Coper-nicium", "[285]"),
    "Nh":	("Nihon-ium", "[286]"),
    "Fl":	("Flerov-ium", "[289]"),
    "Mc":	("Moscov-ium", "[290]"),
    "Lv":	("Liver-morium", "[293]"),
    "Ts":	("Tenness-ine", "[294]"),
    "Og":	("Oga-nesson", "[294]"),
    "La":	("Lan-thanum", "138.91"),
    "Ce":	("Cerium", "140.12"),
    "Pr":	("Praseo-dymium", "140.91"),
    "Nd":	("Neo-dymium", "144.24"),
    "Pm":	("Prome-thium", "[145]"),
    "Sm":	("Sama-rium", "150.36"),
    "Eu":	("Europ-ium", "151.96"),
    "Gd":	("Gadolin-ium", "157.25"),
    "Tb":	("Ter-bium", "158.93"),
    "Dy":	("Dyspro-sium", "162.50"),
    "Ho":	("Hol-mium", "164.93"),
    "Er":	("Erbium", "167.26"),
    "Tm":	("Thulium", "168.93"),
    "Yb":	("Ytter-bium", "173.05"),
    "Ac":	("Actin-ium", "[227]"),
    "Th":	("Thor-ium", "232.04"),
    "Pa":	("Protac-tinium", "231.04"),
    "U":	("Ura-nium", "238.03"),
    "Np":	("Neptu-nium", "[237]"),
    "Pu":	("Pluto-nium", "[244]"),
    "Am":	("Ameri-cium", "[243]"),
    "Cm":	("Curium", "[247]"),
    "Bk":	("Berkel-ium", "[247]"),
    "Cf":	("Califor-nium", "[251]"),
    "Es":	("Einstei-nium", "[252]"),
    "Fm":	("Fer-mium", "[257]"),
    "Md":	("Mende-levium", "[258]"),
    "No":	("Nobel-ium", "[259]"),
}


class Elements(dict):
    """ Atoms list processor
    """
    # pylint: disable=line-too-long

    def __init__(self, alist, **kwargs):
        dict.__init__(self, {"by-name": alist}, **kwargs)
        self._atoms, self._by_id = {}, {}
        self._msg = self._process()

    def named(self, key:str=""):
        if not key:
            return self._atoms
        return self._atoms[key]

    def last_message(self) -> str:
        """ Returns the last message; empty if all ok. """
        return self._msg

    def _process(self):
        dct, new = {}, {}
        anames = self.get("by-name")
        assert isinstance(anames, list)
        for item in anames:
            an_id = item["Id"]
            assert isinstance(an_id, int)
            symbol = item["Key"]
            if "-" in symbol or not symbol:
                continue
            if symbol not in ATOMS:
                return f"Weird atom: {symbol}"
            if item["Weight"] in dct:
                return f"Dup={item}"
            dct[item["Weight"]] = item
            if symbol in new:
                return f"Dup symbol: {item}"
            new[symbol] = item
            if "Wsa" not in new[symbol]:
                continue
            new[symbol]["Wsa"] = ATOMS[symbol][1]
            if not an_id:
                continue
            if an_id in self._by_id:
                return f"Dup Id: {an_id}, for {item}"
            self._by_id[an_id] = Atom(item=item)
        self._atoms = new
        return ""

    def by_weight(self) -> list:
        """ Returns a list formed by triplets, ordered by 'weight'. """
        items = self.get("by-name")
        if not items:
            return []
        there = [(item["Key"], item["Weight"], item) for item in items if item["Weight"]]
        alist = sorted(there, key=lambda x: x[1])
        # e.g. ('H', 1, {'Id': 1101, 'Key': 'H', ...})
        return alist

    def by_id(self) -> dict:
        """ Returns atoms by Id. """
        return self._by_id


class Atom():
    """ Atom/ Element, class helper. """
    def __init__(self, symbol:str="", item=None):
        sample = {
            "Id": 1101,
            "Key": "H",
            "Title": "Hydrogen",
            "Trivial": None,
            "Weight": 1,
            "Wsa": ""
        }
        assert sample["Id"] == 1101
        if item:
            assert not symbol
            self.props = item
            if not item["Wsa"]:
                item["Wsa"] = ATOMS[symbol][1]
        else:
            self._from_symbol(symbol)

    def standard_atomic_weight(self) -> float:
        wsa = self.props["Wsa"]
        if not wsa:
            return 0.0
        return float(wsa)

    def n_protons(self) -> int:
        """ Return the number of protons, -1 if unknown.
        """
        weight = self.props["Weight"]
        return weight if weight else -1

    def n_neutrons(self) -> int:
        """ Return the number of neutrons: N + P = A,
        Or -1 if unknown.
        """
        protons = self.n_protons()
        if protons <= 0:
            return -1
        wsa = round(self.standard_atomic_weight())
        return wsa - protons

    def _from_symbol(self, symbol:str):
        assert symbol
        self.props = {
            "Id": 0,
            "Key": symbol,
            "Title": ATOMS[symbol][0].replace("-", ""),
            "Trivial": None,
            "Weight": -1,
            "Wsa": ATOMS[symbol][1],
        }

    def __str__(self) -> str:
        return self.props["Key"]

    def __repr__(self) -> str:
        return "'" + self.props["Key"] + "'"


# Main script
if __name__ == "__main__":
    print("Please import me!")
