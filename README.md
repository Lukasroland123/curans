# Curans — site 2

Psykoterapi, familiebehandling, traumebehandling, bisidderstøtte og
supervision ved Lotte Stegeager. Søstersite til `../site/`
(Hesteassisteret Praksis), bygget på præcis samme opskrift.

**Status: bygget lokalt, ikke i luften.** Den venter på domænet.

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

**322 redigerbare felter** fordelt på 9 sider.

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

### Venter på domænet

- [ ] **`curans.dk` er ikke aktiv endnu.** DK Hostmaster har den som
      *Reserved*. Registranten kan hverken ses eller ændres, før den er Active
- [ ] **Ejerskifte.** one.com har `Lukas Stegeager` som ejer. Den skal stå i
      **Lottes** navn som de to andre domæner. Rettes under Mine produkter →
      Administrer → Skift domænets ejerinformationer, når domænet er aktivt
- [ ] Zonen i Cloudflare, Pages-projekt, custom domain
- [ ] **`curans.dk` og `www.curans.dk` skal tilføjes `ALLOWED_DOMAINS`** i
      Cloudflare-workeren `sveltia-cms-auth`. Den matcher ikke underdomæner,
      og uden dem dør Lottes login uden en fejlbesked — den slags tog en time
      sidste gang
- [ ] Nyt **offentligt** GitHub-repo `Lukasroland123/curans`. Navnet står
      allerede i `config.yml`; ændres det, skal linjen rettes med
- [ ] `lotte@curans.dk` som **alias på den eksisterende Microsoft 365-postkasse**
      gennem DanDomain. Adressen står allerede i `site.json`, så den skal
      virke, før siden går i luften

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

- [ ] **Person-`@id` skal pege samme sted.** Schemaet her siger, at det
      kanoniske id for Lotte er `https://curans.dk/#lotte`, fordi Curans bliver
      det juridiske firmanavn for begge grene. Site 1 bruger i dag
      `https://hesteassisteret-praksis.dk/#lotte`. Peger de ikke samme sted,
      ser en maskine to forskellige mennesker
- [ ] `site.json` på site 1: `email`, `juridisk_navn`, `soestersite_navn`,
      `soestersite_url` og `google_anmeldelser`
- [ ] Søsterblokken på site 1 nævner i dag gren 2's **ydelser**. Efter reglen i
      `SEO-OG-GEO.md` må den kun nævne **praksissen** — én sætning og et link

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
