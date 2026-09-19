# -*- coding: utf-8 -*-
"""
Bygger src/admin/config.yml ud fra datafilerne i src/_data/.

Hvorfor et script og ikke en haandskrevet fil: paa soestersitet blev fem felter
glemt i config.yml, og de var usynlige for Lotte, indtil nogen opdagede det.
Naar filen genereres fra dataene, KAN et felt ikke blive glemt.

Koeres med:  python scripts/lav-cms-config.py
Kontrolleres med:  python scripts/tjek-cms-felter.py

Labels: scriptet gaetter en dansk etiket ud fra noeglens navn. Er en etiket
daarlig, rettes den i ETIKETTER herunder - ikke i config.yml, for den bliver
overskrevet naeste gang scriptet koeres.
"""
import io
import json
import os

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROD, "src", "_data")
UD = os.path.join(ROD, "src", "admin", "config.yml")

REPO = "Lukasroland123/curans"
WORKER = "https://sveltia-cms-auth.lukas-rs-arbejde.workers.dev"

# Siderne i den raekkefoelge, Lotte skal se dem. Navnet til venstre er
# filnavnet i _data, og det SKAL matche "side" i den tilhoerende .njk-fil,
# for det er det, "Rediger denne side"-knappen linker til.
SIDER = [
    ("forside", "Forside", "Den første side, folk lander på."),
    ("terapi", "Individuel terapi", "Siden om samtaleforløb ved stress, angst og livskriser."),
    ("traumebehandling", "Traumebehandling", "Siden om choktraumer (PTSD) og komplekse traumer."),
    ("familiebehandling", "Familiebehandling", "Siden om forløb for hele familien."),
    ("bisidderstoette", "Bisidderstøtte", "Siden om at gå med som bisidder til møder."),
    ("supervision", "Supervision", "Siden om supervision af personalegrupper."),
    ("priser", "Priser", "Priser, åbningstider og beliggenhed."),
    ("omlotte", "Om Lotte", "Din egen side: uddannelse, erfaring og tilgang."),
    ("kontakt", "Kontakt", "Telefon, adresse, åbningstider og tavshedspligt."),
]

# Faste etiketter for de noegler, der gaar igen. Nøglen matches foerst helt,
# derefter paa endelse, derefter paa forstavelse.
ETIKETTER = {
    "titel": "Sidens titel i Google (ses ikke på siden)",
    "beskrivelse": "Sidens beskrivelse i Google (ses ikke på siden)",
    "ydelse_navn": "Ydelsens navn (bruges kun af søgemaskiner)",
    "svar": "Det korte svar (den grå boks øverst)",
    "citat": "Citat",
    "citat_kilde": "Hvem sagde det?",
    "udtalelse": "Udtalelse",
    "udtalelse_hvem": "Hvem siger det?",
    # Listerne faar deres egne etiketter - de automatiske blev for tekniske.
    "hero_maerkater": "De små mærkater under knapperne",
    "ydelser_kort": "De fem kort med ydelser",
    "udtalelser": "Udtalelser fra klienter",
    "hvem_kort": "Kortene under »Hvem er det for«",
    "tilskud_kort": "Kortene om hvem der kan betale",
    "typer_kort": "De to kort om traumetyper",
    "metode_punkter": "Punktopstillingen under »Sådan foregår det«",
    "sparring_personer": "Samarbejdspartnere",
    "betingelser": "Punkterne om åbningstider og tillæg",
    "litteratur": "Litteraturlisten",
    "uddannelser": "Uddannelser og kurser",
    "kort": "Priskortene",
    "faq": "Spørgsmål og svar",
}

ENDELSER = [
    ("_mikrotekst", "Lille tekst over overskriften"),
    ("_overskrift", "Overskrift"),
    ("_underrubrik", "Underoverskrift"),
    ("_intro", "Introtekst"),
    ("_indledning", "Indledende tekst"),
    ("_afslutning", "Afsluttende tekst"),
    ("_tekst", "Tekst"),
    ("_billede2_alt", "Billede 2 · hvad ser man på det?"),
    ("_billede2tekst", "Billede 2 · billedtekst"),
    ("_billede2", "Billede 2 (kun hvis teksten er lang)"),
    ("_billede_alt", "Hvad ser man på billedet?"),
    ("_billedtekst", "Billedtekst (vises under billedet)"),
    ("_billede", "Billede"),
    ("_boks_titel", "Fremhævet boks · fed indledning"),
    ("_boks_tekst", "Fremhævet boks · resten af teksten"),
    ("_knap", "Tekst på knappen"),
    ("_knap1", "Tekst på den orange knap"),
    ("_knap2", "Tekst på den hvide knap"),
    ("_titel", "Overskrift"),
    ("_hvem", "Hvem siger det?"),
    ("_efter", "Tekst efter citatet"),
]

FORSTAVELSER = [
    ("hero_", "Øverst på siden · "),
    ("metode_", "Sådan foregår det · "),
    ("hvem_", "Hvem er det for · "),
    ("hvad_", "Hvad er det · "),
    ("etik_", "Etisk afsæt · "),
    ("typer_", "De to slags traumer · "),
    ("faq_", "Spørgsmål og svar · "),
    ("kryds_", "Boks med link til den anden hjemmeside · "),
    ("cta_", "Grøn boks nederst · "),
    ("ydelser_", "Ydelseskortene · "),
    ("udtalelser_", "Udtalelser · "),
    ("omlotte_", "Om Lotte-afsnittet · "),
    ("tilskud_", "Hvem kan betale · "),
    ("beliggenhed_", "Beliggenhed · "),
    ("lov_", "Lovteksten · "),
    ("uddannelser_", "Uddannelse · "),
    ("erfaring_", "Erfaring · "),
    ("tilgang_", "Faglige tilgange · "),
    ("sparring_", "Samarbejdspartnere · "),
    ("aabningstider_", "Åbningstider · "),
    ("tavshed_", "Tavshedspligt · "),
    ("praktisk_", "Sådan finder du mig · "),
    ("gratis_", "Den gratis samtale · "),
    ("kort_", "Priskortene · "),
    ("litteratur_", "Litteraturlisten · "),
]

# Felter der skal vaere flerlinjede. Alt andet under 90 tegn bliver en enkelt linje.
LANGE = ("_tekst", "_intro", "_indledning", "_afslutning", "svar", "_citat", "_efter")


def etiket(noegle):
    if noegle in ETIKETTER:
        return ETIKETTER[noegle]
    forstavelse = ""
    for f, tekst in FORSTAVELSER:
        if noegle.startswith(f):
            forstavelse = tekst
            break
    for e, tekst in ENDELSER:
        if noegle.endswith(e):
            return forstavelse + tekst
    rest = noegle
    for f, _ in FORSTAVELSER:
        if noegle.startswith(f):
            rest = noegle[len(f):]
            break
    return forstavelse + rest.replace("_", " ").capitalize()


def widget(noegle, vaerdi):
    if noegle.endswith("_billede") or noegle.endswith("_billede2"):
        return "image"
    if isinstance(vaerdi, str):
        if any(noegle.endswith(l) or noegle == l for l in LANGE):
            return "text"
        if "\n" in vaerdi or len(vaerdi) > 90:
            return "text"
    return "string"


def esc(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def felt_linje(noegle, vaerdi, indryk):
    w = widget(noegle, vaerdi)
    # Et billede maa ALTID kunne fjernes igen. Var feltet paakraevet, fordi
    # der tilfaeldigvis ligger et foto i det i dag, kunne Lotte ikke tage
    # fotoet ud og faa den groenne plads tilbage.
    paakraevet = "" if vaerdi and w != "image" else ", required: false"
    hint = ""
    if noegle.endswith("_billede_alt"):
        hint = (', hint: "Læses højt for blinde og bruges af Google i stedet for '
                'billedet. Beskriv hvad man SER, ikke stemningen."')
    if noegle.endswith("_billede2"):
        hint = (', hint: "Et billede mere i samme spalte. Brug det, når teksten '
                'ved siden af er lang. Lad det stå tomt, og der vises en grøn '
                'plads i stedet. Den vises kun, hvis billede 1 er udfyldt."')
    elif noegle.endswith("_billede"):
        hint = (', hint: "Lad feltet stå tomt, og der vises en grøn plads, '
                'der venter på et foto. Siden går ikke i stykker af det."')
    if noegle.endswith("_billede2tekst") or noegle.endswith("_billedtekst"):
        hint = (', hint: "Den kursive tekst under billedet. Lad feltet stå tomt, '
                'hvis der ingen tekst skal være."')
    return "%s- { name: %s, label: %s, widget: %s%s%s }" % (
        " " * indryk, noegle, esc(etiket(noegle)), w, paakraevet, hint)


def liste_blok(noegle, liste, indryk):
    ud = []
    i = " " * indryk
    ud.append("%s- name: %s" % (i, noegle))
    ud.append("%s  label: %s" % (i, esc(etiket(noegle))))
    ud.append("%s  widget: list" % i)
    # Laast antal: Lotte kan rette indholdet, men ikke antallet af kort.
    # Skal der vaere flere, tilfoejer Lukas et element i JSON-filen.
    ud.append("%s  allow_add: false" % i)
    ud.append("%s  allow_remove: false" % i)
    ud.append("%s  fields:" % i)
    if liste and isinstance(liste[0], dict):
        for k, v in liste[0].items():
            ud.append(felt_linje(k, v, indryk + 4))
    else:
        ud.append("%s    - { name: tekst, label: \"Tekst\", widget: string }" % i)
    return ud


def main():
    linjer = [
        "# =====================================================================",
        "#  Redigeringssystem for Curans",
        "#",
        "#  DENNE FIL ER GENERERET. Ret den ikke i hånden - kør i stedet",
        "#      python scripts/lav-cms-config.py",
        "#  og ret etiketterne i det script. Ellers forsvinder rettelsen næste",
        "#  gang, nogen kører scriptet.",
        "# =====================================================================",
        "",
        "backend:",
        "  name: github",
        "  repo: %s" % REPO,
        "  branch: main",
        "",
        "  # Login gaar gennem vores egen Cloudflare Worker (sveltia-cms-auth),",
        "  # den samme som soestersitet bruger. HUSK at tilfoeje curans.dk og",
        "  # www.curans.dk til ALLOWED_DOMAINS i Workeren - den matcher ikke",
        "  # underdomaener, og uden dem doer login uden en fejlbesked.",
        "  base_url: %s" % WORKER,
        "",
        "  commit_messages:",
        '    update: "Rettet {{collection}} · {{author-name}}"',
        '    uploadMedia: "Nyt billede: {{path}}"',
        '    deleteMedia: "Slettet billede: {{path}}"',
        "",
        'media_folder: "src/billeder"',
        'public_folder: "/billeder"',
        "",
        "collections:",
        "  - name: sider",
        '    label: "Sider"',
        "    files:",
    ]

    i_felter = 0
    for navn, label, beskrivelse in SIDER:
        sti = os.path.join(DATA, navn + ".json")
        data = json.load(io.open(sti, encoding="utf-8"))
        linjer.append("")
        linjer.append("      - name: %s" % navn)
        linjer.append("        label: %s" % esc(label))
        linjer.append('        file: "src/_data/%s.json"' % navn)
        linjer.append("        description: %s" % esc(beskrivelse))
        linjer.append("        fields:")
        for k, v in data.items():
            if isinstance(v, list):
                linjer.extend(liste_blok(k, v, 10))
                i_felter += len(v[0]) if v and isinstance(v[0], dict) else 1
            else:
                linjer.append(felt_linje(k, v, 10))
                i_felter += 1

    # Fælles oplysninger ligger for sig, saa de ikke drukner i sidernes felter.
    sti = os.path.join(DATA, "site.json")
    data = json.load(io.open(sti, encoding="utf-8"))
    linjer.append("")
    linjer.append("  - name: faelles")
    linjer.append('    label: "Fælles oplysninger"')
    linjer.append("    files:")
    linjer.append("      - name: site")
    linjer.append('        label: "Navn, adresse og kontakt"')
    linjer.append('        file: "src/_data/site.json"')
    linjer.append('        description: "Står i bunden af alle sider. Rettes ét sted."')
    linjer.append("        fields:")
    faelles_etiketter = {
        "navn": "Hjemmesidens navn",
        "juridisk_navn": "Virksomhedens juridiske navn (som på VIRK)",
        "undertitel": "Undertitel under navnet",
        "domaene": "Hjemmesidens adresse",
        "telefon": "Telefonnummer, som det skal se ud",
        "telefon_link": "Telefonnummer til opkaldsknappen",
        "cvr": "CVR-nummer",
        "forening_navn": "Faglig forening",
        "forening_url": "Foreningens hjemmeside",
        "email": "E-mailadresse",
        "adresse": "Vej og husnummer",
        "postnr_by": "Postnummer og by",
        "facebook": "Link til Facebook",
        "google_anmeldelser": "Link til anmeldelserne på Google",
        "soestersite_url": "Adressen på den anden hjemmeside",
        "soestersite_navn": "Navnet på den anden hjemmeside",
        "footer_beskrivelse": "Kort beskrivelse nederst på siden",
        "cta_knap": "Tekst på den orange knap i menuen",
    }
    for k, v in data.items():
        w = "text" if len(str(v)) > 90 else "string"
        linjer.append('          - { name: %s, label: "%s", widget: %s }'
                      % (k, faelles_etiketter.get(k, k), w))
        i_felter += 1

    io.open(UD, "w", encoding="utf-8").write("\n".join(linjer) + "\n")
    print("Skrevet %s" % UD)
    print("%d redigerbare felter fordelt paa %d sider" % (i_felter, len(SIDER)))


if __name__ == "__main__":
    main()
