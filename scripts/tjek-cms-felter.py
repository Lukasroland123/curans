# -*- coding: utf-8 -*-
"""
Kontrollerer, at HVERT felt i src/_data/*.json ogsaa findes i
src/admin/config.yml - ogsaa felterne inde i lister.

Baggrunden: paa soestersitet blev fem felter glemt i CMS'et. De var usynlige
for Lotte, og fejlen blev foerst opdaget, da nogen ledte efter et felt, der
ikke var der. Den fejl skal ikke kunne gentage sig her.

Koeres med:  python scripts/tjek-cms-felter.py
Slutter med kode 1, hvis noget mangler, saa den kan bruges i CI.
"""
import io
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml mangler. Koer:  pip install pyyaml")

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROD, "src", "_data")
CONFIG = os.path.join(ROD, "src", "admin", "config.yml")


def felter_i_json(obj, praefiks=""):
    """Alle bladnoegler i en datafil, som 'noegle' eller 'liste[].noegle'."""
    ud = set()
    for k, v in obj.items():
        if isinstance(v, list):
            if v and isinstance(v[0], dict):
                for uk in v[0]:
                    ud.add("%s%s[].%s" % (praefiks, k, uk))
            else:
                ud.add("%s%s[]" % (praefiks, k))
        else:
            ud.add(praefiks + k)
    return ud


def felter_i_config(felter, praefiks=""):
    ud = set()
    for f in felter or []:
        navn = f.get("name")
        if not navn:
            continue
        if f.get("widget") == "list":
            under = f.get("fields")
            if under:
                for u in under:
                    ud.add("%s%s[].%s" % (praefiks, navn, u.get("name")))
            else:
                ud.add("%s%s[]" % (praefiks, navn))
        else:
            ud.add(praefiks + navn)
    return ud


def main():
    cfg = yaml.safe_load(io.open(CONFIG, encoding="utf-8"))
    i_cms = {}
    for samling in cfg["collections"]:
        for fil in samling.get("files", []):
            # "src/_data/forside.json" -> "forside"
            navn = os.path.basename(fil["file"]).replace(".json", "")
            i_cms[navn] = felter_i_config(fil.get("fields"))

    fejl = 0
    for filnavn in sorted(os.listdir(DATA)):
        if not filnavn.endswith(".json"):
            continue
        navn = filnavn[:-5]
        data = json.load(io.open(os.path.join(DATA, filnavn), encoding="utf-8"))
        i_json = felter_i_json(data)

        if navn not in i_cms:
            print("MANGLER HELT: %s.json er ikke i config.yml" % navn)
            fejl += 1
            continue

        mangler = i_json - i_cms[navn]
        ekstra = i_cms[navn] - i_json
        if mangler:
            print("%s: %d felter mangler i CMS'et:" % (navn, len(mangler)))
            for m in sorted(mangler):
                print("   - %s" % m)
            fejl += len(mangler)
        if ekstra:
            print("%s: %d felter i CMS'et findes ikke i JSON'en:" % (navn, len(ekstra)))
            for e in sorted(ekstra):
                print("   - %s" % e)
            fejl += len(ekstra)
        if not mangler and not ekstra:
            print("%-20s OK  (%d felter)" % (navn, len(i_json)))

    if fejl:
        print("\n%d problemer. Koer scripts/lav-cms-config.py." % fejl)
        sys.exit(1)
    print("\nAlt stemmer. Ingen felter er glemt.")


if __name__ == "__main__":
    main()
