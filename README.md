# BUR Víkingur — WordPress eining

Kyrrstæð HTML-eining fyrir "Barna- og unglingaráð" (BUR) hjá Knattspyrnufélaginu
Víkingi. Hannað til að líma beint inn í eina **Custom HTML** blokk í WordPress.

Síðan sýnir:
- Tengla á skjöl (PDF)
- Stjórn BUR með netföngum
- Alla aldursflokka (2.–7. flokkur) í fellilista, með foreldraráðum,
  æfingatöflum og helstu mótum

## Skrárnar í þessu safni

| Skrá | Hlutverk |
|---|---|
| `bur-innihald.json` | **Heimildarskráin.** Öll gögn — nöfn, netföng, æfingatöflur, mót, skjöl. Þessari skrá á að breyta. |
| `template.html` | Grunnbygging/stíll (CSS/JS) síðunnar. Inniheldur `__CONTENT__` sem build.py fyllir út. |
| `build.py` | Python-forskrift sem býr til `bur-eining.html` úr hinum tveimur skránum. |
| `bur-eining.html` | **Útkoman.** Þetta er skráin sem á að líma inn í WordPress. Sjálfvirkt búin til — ekki breyta henni beint, breytingar týnast við næstu keyrslu. |
| `_content.html` | Hjálparskjal (aðeins innihaldið, án stíla) sem build.py skrifar líka — ekki notað beint og er í `.gitignore`. |

## Hvernig á að uppfæra innihald

1. Opnaðu `bur-innihald.json` og breyttu því sem á við (t.d. bættu við
   nafni/netfangi í foreldraráði, breyttu æfingatíma, uppfærðu `meta.uppfaert`
   dagsetninguna).
2. Keyrðu í þessari möppu:
   ```bash
   python3 build.py
   ```
   Þetta skrifar nýja útgáfu af `bur-eining.html` (og `_content.html`).
3. Opnaðu `bur-eining.html`, afritaðu **allt innihald** skráarinnar.
4. Í WordPress: farðu í síðuna/undirsíðuna sem á að birta þetta, bættu við
   blokk með **"Custom HTML"** (leitaðu að því í Gutenberg — EKKI venjulega
   málsgrein/Texti-blokk, því hún fjarlægir oft `<script>`/stíla af
   öryggisástæðum) og límdu innihaldinu inn þar.
5. Uppfærðu (Update/Uppfæra) síðuna í WordPress.

Ef þú ert eingöngu að breyta útliti (litum, letri, dálkum o.s.frv.) skaltu
breyta `template.html` og keyra `build.py` aftur á sama hátt.

## Uppbygging `bur-innihald.json`

```jsonc
{
  "meta": { "uppfaert": "2026-09-09" },
  "hero": { "yfirsogn": "...", "titill": "...", "inngangur": "..." },
  "skjol": [ { "titill": "...", "slod": "https://..." } ],
  "stjorn": {
    "titill": "Stjórn barna- og unglingaráðs ...",
    "medlimir": [ { "nafn": "...", "hlutverk": "...", "netfang": "..." } ]
  },
  "flokkar": [
    {
      "id": "f2",
      "heiti": "2. flokkur",
      "foreldrarad": {
        "kk": [ { "nafn": "...", "netfang": "..." } ],
        "kvk": [ { "nafn": "...", "netfang": "..." } ]
      },
      "æfingatafla": {
        "kk":  [ { "dagur": "Mánudagar", "timi": "18:15–19:30", "stadur": "Víkin – Gervigras" } ],
        "kvk": [ ... ]
      },
      "helstu_mot": "Reykjavíkurmót, Íslandsmót ..."
    }
  ]
}
```

Athugasemdir:
- `netfang` má sleppa (skilur eftir „—" í stað tengils á póst).
- `æfingatafla` má sleppa alveg fyrir flokk sem hefur enga birta æfingatöflu.
- Fyrsti flokkurinn í `flokkar`-fylkinu er sjálfkrafa opinn (fellilisti) þegar
  síðan hleðst.

## Athugasemdir um JavaScript og WordPress-þemu

- Skriftan í `template.html` er **framsækin viðbót** (progressive enhancement):
  ef WordPress eða öryggisviðbót fjarlægir `<script>` keyrir síðan samt sem
  áður, birtir bara alla flokka opna í einu í staðinn fyrir fellilista.
- Sumar WordPress-þemur (t.d. Avada/Fusion) setja "scroll reveal"
  hreyfimyndir utan um efnisdálka sem geta fest einingunni á nær-0 gegnsæi
  (ósýnileg síða). Bæði CSS-regla og MutationObserver í skriftunni verja
  gegn þessu sérstaklega fyrir foreldra sem innihalda `.bur-wp`.
- Í lokaskránni (`bur-eining.html`) eru allar auðar línur fjarlægðar til að
  koma í veg fyrir að `wpautop()` í WordPress breyti þeim í `</p><p>` inni í
  `<style>`/`<script>` kubbum, sem myndi eyðileggja útlit og virkni hljóðlega.

## Athugið — persónuupplýsingar

`bur-innihald.json` og þar með `bur-eining.html` innihalda nöfn og netföng
foreldra/forráðamanna og stjórnarmeðlima. Geymið þetta git-safn **einkaeign
(private)** á GitHub.
