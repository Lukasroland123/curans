# Curans — site 2

Psykoterapi, familiebehandling, traumebehandling, bisidderstøtte og
supervision ved Lotte Stegeager. Søstersite til `../site/`
(Hesteassisteret Praksis), bygget på præcis samme opskrift.

**Status: I LUFTEN på `https://curans.dk` siden 20-09-2026.**

---

## Kør lokalt

```powershell
cd "C:\Users\Lukas\Desktop\Mor Virksomhed\curans"
npm install     # kun første gang
npm start       # http://localhost:8013
```

Port 8013, så den kan køre samtidig med site 1 på 8012. Brug
**Ctrl+Shift+R** til at opdatere, ikke F5.

---

## Siderne

```
Forside                     /
Terapi ▾
  ├ Individuel terapi       /terapi/
  ├ Traumebehandling        /traumebehandling/
  └ Familiebehandling       /familiebehandling/
Støtte & supervision ▾
  ├ Bisidderstøtte          /bisidderstoette/
  └ Supervision             /supervision/
Priser                      /priser/
Om Lotte                    /om-lotte/
Kontakt                     /kontakt/
[Book uforpligtende samtale]

/privatlivspolitik/         kun i footeren, ikke i CMS'et
/404.html                   teknisk fejlside, ikke i CMS'et
```

**345 redigerbare felter** fordelt på 9 sider.

---

## Redigeringssystemet

Samme som site 1: Eleventy 3 + Sveltia CMS, indhold i `src/_data/*.json`,
design i `src/*.njk`. Lotte redigerer kun JSON'en gennem `/admin`.

**`src/admin/config.yml` er genereret, ikke håndskrevet.**

```powershell
python scripts/lav-cms-config.py      # bygger config.yml ud fra _data
python scripts/tjek-cms-felter.py     # kontrollerer at intet felt mangler
```

Det er en direkte konsekvens af fejlen på site 1, hvor fem felter blev glemt
i `config.yml` og var usynlige for Lotte, indtil nogen tilfældigt ledte efter
et af dem. Når filen genereres fra dataene, kan et felt ikke blive glemt.
Skal en etiket rettes, rettes den i `lav-cms-config.py` — ikke i `config.yml`,
for den bliver overskrevet.

---

## Det mangler, før den kan gå i luften

### ✅ Gjort 20-09-2026 — den gik i luften

- [x] **`curans.dk` er aktiv** og står i **Lottes** navn i DK Hostmasters
      register. Kontrolleret i whois, ikke gættet. one.coms
      "Overdragelse af webhotel og domæne" er en anden ting og skal ikke
      bruges — den flytter one.com-kontoen, ikke registranten
- [x] **Zonen, Pages-projektet og custom domain.** `curans.dk` og
      `www.curans.dk` er Active med gyldigt certifikat.
      **Fælde, hvis det skal gøres igen:** one.coms gamle A-poster følger
      med ved importen og vinder over Pages. De skal slettes, før custom
      domain kan slå igennem. Det samme gælder deres `MX .`, som betyder
      "her modtages ingen mail" og spærrer for mailopsætningen
- [x] **Lotte er tilføjet som medarbejder på repoet** 20-09-2026 med
      skriveadgang, som på site 1. **Invitationen skal accepteres i mailen
      fra GitHub** — før det kan hun logge ind i `/admin` og se det hele,
      men ikke gemme

### Mangler stadig

- [ ] **`ALLOWED_DOMAINS` i workeren `sveltia-cms-auth` er aldrig
      afprøvet på `curans.dk`.** Log ind på `curans.dk/admin` én gang og se
      om det virker, **før** Lotte får adressen. Uden `curans.dk` og
      `www.curans.dk` i listen dør login uden en fejlbesked — det tog en
      time sidste gang
- [ ] `lotte@curans.dk`. **Blokeret** — se `../TO-DO-LISTE.md`, afsnittet
      om MFA og fejl 399287

- [x] ~~Nyt **offentligt** GitHub-repo `Lukasroland123/curans`.~~ Oprettet
      19-09-2026, præcis som site 1. Det lå privat en halv time, men blev
      lagt offentligt igen: privat kræver, at Cloudflare Pages får adgang
      til netop det repo, og at workeren `sveltia-cms-auth` beder om
      `repo`-scope og ikke `public_repo`. Offentligt sparer begge dele

### Venter på Lotte

- [ ] **Navnet på VIRK.** `juridisk_navn` står som "Curans v/Lotte Stegeager"
      — det skal matche det, der faktisk kommer til at stå på VIRK
- [ ] **Prisen.** Den gamle side sagde **965 kr.**, site 1 siger **968 kr.**
      Tre kroners forskel. Skal det være det samme tal begge steder?
- [ ] **Supervisionssiden skal læses igennem.** Den gamle side var *ufærdig* —
      der stod bogstaveligt `Text element` og `,,,,,` live, og overskrifterne
      "Hvem kan henvende sig?" og "Hvordan foregår det?" havde ingen tekst
      under sig. Det, der står her nu, er skrevet ud fra det ene rigtige
      afsnit, der var. Hun skal godkende det
- [ ] **Studiestøtte.** `TO-DO-LISTE.md` regner den med som en ydelse, men den
      har aldrig haft en side. Enten skrives den, eller også ryger den ud
- [ ] **Afbudsregler.** Stod ikke på den gamle side. Bør på prissiden, som på
      site 1
- [ ] **Der mangler billeder. 11 rammer står tomme.** Stockfotoene fra den
      gamle side er slettet 19-09-2026. De var købt af Fokus, og en
      stocklicens følger den, der købte den — ikke domænet. Vi ved ikke, hvad
      der er købt, så de kunne ikke tages med over.

      Tilbage er **ti billeder, som alle er Lottes egne**: hendes stue,
      tavlerne, figurerne på bordet, flipoveren, portrættet og kunstværket.

      Sådan ser det ud nu:

      | Side | Billeder | Tomme rammer |
      |---|---|---|
      | Forside | 1 | 1 |
      | Terapi | 2 | 2 |
      | Traumebehandling | 1 | 2 |
      | Familiebehandling | 2 | 1 |
      | Bisidderstøtte | 1 | 1 |
      | Supervision | **0** | 2 |
      | Priser | 1 | 0 |
      | Om Lotte | 2 | 1 |
      | Kontakt | 0 | 1 |

      Supervisionssiden har ingen billeder overhovedet. Traumesiden har kun
      kunstværket. Lotte skal tage nogle fotos, eller også skal der købes nye
      med en licens, I selv ejer — Unsplash og Pexels er gratis og frie.

      Felterne står klar i CMS'et, så hun kan lægge dem ind selv.

- [ ] **Billedernes opløsning.** Ingen af filerne er bredere end 1.423 px,
      fordi det er Fokus' nedskalerede kopier. Originalerne findes kun på
      Lottes telefon
- [ ] Korrekturlæsning af det hele

### Skal gøres på site 1, før site 2 går i luften

**Alle tre er gjort 19-09-2026** (`2105e68` på site 1, `9754462` her).
Teksten står tilbage, fordi den forklarer hvorfor.

- [x] **Person-`@id` skal pege samme sted.** Schemaet her siger, at det
      kanoniske id for Lotte er `https://curans.dk/#lotte`, fordi Curans bliver
      det juridiske firmanavn for begge grene. Site 1 bruger i dag
      `https://hesteassisteret-praksis.dk/#lotte`. Peger de ikke samme sted,
      ser en maskine to forskellige mennesker
- [x] `site.json` på site 1: `juridisk_navn`, `soestersite_navn` og
      `soestersite_url` følger navneskiftet. `google_anmeldelser` er lagt om,
      se nedenfor. **`email` mangler stadig** — den venter på aliasset
      `lotte@curans.dk`, og en død adresse må ikke udgives
- [x] Søsterblokken på site 1 nævnte gren 2's **ydelser**. Alle fire blokke er
      nu én sætning uden overskrift, efter reglen i `SEO-OG-GEO.md`

---

## Google-profilen og anmeldelserne

Anmeldelserne er det eneste i hele flytningen, der **ikke kan genskabes**.
De kan hverken flyttes, kopieres eller eksporteres mellem profiler. Derfor
den ene regel, som ikke skal tages op igen: **profilen døbes om, den
oprettes ikke forfra.** Et navneskift beholder anmeldelser, bedømmelse,
billeder, spørgsmål og åbningsdato. En ny profil starter på nul og
konkurrerer med den gamle om den samme adresse.

Begrundelsen i sin fulde længde står i `../SEO-OG-GEO.md`, trin 3.

**Linket, 19-09-2026.** Begge sites har en knap "Læs anmeldelserne på
Google" under udtalelserne. Den pegede på en Maps-søgning efter **navnet**
`Narrativ Samtale` og ville være døet i det sekund, profilen blev døbt om.
Den peger nu på profilens **place-id**, som aldrig ændrer sig:

    https://www.google.com/maps/place/?q=place_id:ChIJ8W5MEKNhUkYRLoMqUvTlLY4

Id'erne er hentet af profilens eget delelink 19-09-2026 og noteres her, så
de ikke skal graves frem igen:

| | |
|---|---|
| Place-id | `ChIJ8W5MEKNhUkYRLoMqUvTlLY4` |
| CID | `10245097564851045166` |
| Anmeld-link | `https://g.page/r/CS6DKlL05S2OEBM/review` |

Maps-linket blev valgt frem for `search.google.com/local/reviews`, fordi
den sidste viser tre konkurrenter som annoncer øverst, før Lottes egen
profil. Maps åbner direkte på kortet med bedømmelsen og fanen Anmeldelser.

Skal knappen ændres, er det ét felt i CMS'et — **Indstillinger → Link til
anmeldelserne på Google** — på begge sites. Ingen kode skal røres.

---

## Arbejdsdelingen mellem de to sites

Reglerne står i `../SEO-OG-GEO.md` under "ARBEJDSDELINGEN MELLEM DE TO SITES"
og er fulgt her:

- Heste nævnes **ikke** som en ydelse. Kun i søsterblokken: én sætning og et
  link, aldrig en overskrift og aldrig en liste
- Traumearbejde hedder **"traumebehandling"** her og
  **"traumebearbejdning i et hesteassisteret forløb"** på site 1, så de to
  sider ikke slås om den samme søgning
- Adresse og telefon er **identiske, tegn for tegn**, med site 1

---

## Hvor kom indholdet fra?

Alt er hentet fra den gamle `narrativsamtale.dk` 19. september 2026 og ligger
råt i `../gammelt-indhold/`. Siden er JavaScript-renderet, så teksten måtte
hentes med en styret browser — `curl` giver kun script.

Fakta er bevaret: priser, lovcitater (forvaltningslovens § 8 og kapitel 4),
ICD-11-koderne, uddannelseslisten, litteraturlisten, samarbejdspartnerne og
de tre udtalelser. Resten er strammet op.

**Krediteringen på traumesiden skal blive stående.** Kunstværket er af
C. Barr (@coolcatcate) og er gengivet med særlig tilladelse. Tilladelsen er
knyttet til krediteringen.
