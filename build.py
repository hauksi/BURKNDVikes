#!/usr/bin/env python3
"""
Byggir bur-eining.html úr bur-innihald.json + template.html.
Keyrðu þetta aftur (python3 build.py) í hvert sinn sem bur-innihald.json breytist.

ATH: Skráin sem á að líma inn í "Custom HTML" blokkina í WordPress er
bur-eining.html — EKKI _content.html (sú er bara hjálparskjal með
innihaldinu einu og sér, án útlits/stíla, og virkar ekki ein og sér).

Þarf bæði bur-innihald.json og template.html til að vera í sömu möppu.
"""
import json
import html
import re

with open("bur-innihald.json", encoding="utf-8") as f:
    data = json.load(f)

def esc(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)

def render_name_list(people):
    if not people:
        return '<li class="bur-no-email">Engir skráðir</li>'
    out = []
    for p in people:
        mail = (f'<a href="mailto:{esc(p["netfang"])}">Senda póst</a>'
                if p.get("netfang") else '<span class="bur-no-email">—</span>')
        out.append(f'<li><span>{esc(p["nafn"])}</span>{mail}</li>')
    return "".join(out)

def render_sched_table(rows):
    if not rows:
        return ""
    body = "".join(
        f'<tr><td>{esc(r["dagur"])}</td><td class="bur-time">{esc(r["timi"])}</td><td>{esc(r["stadur"])}</td></tr>'
        for r in rows
    )
    return f'<table class="bur-sched"><tr><th>Dagur</th><th>Tími</th><th>Staður</th></tr>{body}</table>'

def render_flokkur(f, first):
    sched = f.get("æfingatafla")
    sched_html = ""
    if sched:
        sched_html = (
            '<div class="bur-cols" style="margin-top:22px;">'
            f'<div><div class="bur-col-label">Æfingatafla — drengir</div>{render_sched_table(sched["kk"])}</div>'
            f'<div><div class="bur-col-label">Æfingatafla — stúlkur</div>{render_sched_table(sched["kvk"])}</div>'
            '</div>'
        )
    mot_html = (
        f'<div class="bur-mot"><b>Helstu mót:</b> {esc(f["helstu_mot"])}</div>'
        if f.get("helstu_mot") else ""
    )
    open_cls = " open" if first else ""
    aria = "true" if first else "false"
    fr = f["foreldrarad"]
    return (
        f'<div class="bur-acc-item{open_cls}" id="acc-{esc(f["id"])}" data-flokkur="{esc(f["id"])}">'
        f'<div class="bur-acc-head" role="button" tabindex="0" aria-expanded="{aria}">'
        f'<h3>{esc(f["heiti"])}</h3><span class="bur-acc-plus">+</span>'
        '</div>'
        '<div class="bur-acc-body"><div class="bur-acc-in">'
        '<div class="bur-cols">'
        f'<div><div class="bur-col-label">Foreldraráð — drengir</div><ul class="bur-namelist">{render_name_list(fr["kk"])}</ul></div>'
        f'<div><div class="bur-col-label">Foreldraráð — stúlkur</div><ul class="bur-namelist">{render_name_list(fr["kvk"])}</ul></div>'
        '</div>'
        f'{sched_html}{mot_html}'
        '</div></div></div>'
    )

nav_html = '<a href="#bur-sec-skjol">Skjöl</a><a href="#bur-sec-stjorn">Stjórn BUR</a>'
for f in data["flokkar"]:
    nav_html += f'<a href="#acc-{esc(f["id"])}" data-flokkur="{esc(f["id"])}">{esc(f["heiti"])}</a>'

docs_html = "".join(
    f'<a class="bur-doc" href="{esc(d["slod"])}" target="_blank" rel="noopener">'
    f'<span class="bur-doc-ico">PDF</span><span>{esc(d["titill"])}</span></a>'
    for d in data["skjol"]
)

board_html = "".join(
    '<div class="bur-person">'
    f'<div><span class="bur-person-name">{esc(m["nafn"])}</span><span class="bur-person-role">{esc(m["hlutverk"])}</span></div>'
    '<div class="bur-person-actions">'
    + (f'<a class="bur-icobtn" href="mailto:{esc(m["netfang"])}" title="Senda póst" aria-label="Senda póst">&#9993;</a>' if m.get("netfang") else "")
    + (f'<a class="bur-icobtn" href="tel:{esc("".join(c for c in m["simi"] if c.isdigit() or c=="+"))}" title="Hringja" aria-label="Hringja">&#9742;</a>' if m.get("simi") else "")
    + '</div></div>'
    for m in data["stjorn"]["medlimir"]
)

flokkar_html = "".join(render_flokkur(f, i == 0) for i, f in enumerate(data["flokkar"]))

content = f'''<div class="bur-hero">
  <div class="bur-eyebrow">{esc(data["hero"]["yfirsogn"])}</div>
  <h1>{esc(data["hero"]["titill"])}</h1>
  <p>{esc(data["hero"]["inngangur"])}</p>
  <div class="bur-nav" id="bur-nav">{nav_html}</div>
</div>

<div class="bur-section" id="bur-sec-skjol">
  <div class="bur-section-head"><h2>Skjöl</h2></div>
  <div class="bur-docs">{docs_html}</div>
</div>

<div class="bur-section" id="bur-sec-stjorn">
  <div class="bur-section-head"><h2>{esc(data["stjorn"]["titill"])}</h2></div>
  <div class="bur-board">{board_html}</div>
</div>

<div class="bur-section" id="bur-sec-flokkar">
  <div class="bur-section-head"><h2>Aldursflokkar</h2></div>
  <div class="bur-accordion">{flokkar_html}</div>
</div>

<div class="bur-foot">Uppfært {esc(data["meta"]["uppfaert"])} &middot; Knattspyrnufélagið Víkingur</div>'''

with open("_content.html", "w", encoding="utf-8") as f:
    f.write(content)

try:
    with open("template.html", encoding="utf-8") as f:
        template = f.read()
except FileNotFoundError:
    raise SystemExit(
        "Vantar template.html í þessari möppu.\n"
        "Þessi skrá þarf að vera í SÖMU möppu og build.py og bur-innihald.json\n"
        "(t.d. BURKNDVikes-möppunni þinni) — ekki í Downloads eða annars staðar sér.\n"
        "Fáðu template.html frá Claude ef hún vantar."
    )

final_html = template.replace("__CONTENT__", content)

# VÖRN GEGN wpautop(): WordPress-þemu (t.d. Fusion/Avada "Text" einingar) keyra
# oft innihald sem líkist grein/texta í gegnum wpautop(), sem breytir HVERRI
# auðri línu (tvöföldu línubili) í </p><p> — líka INNAN <style> og <script>
# kubba! Það eyðileggur CSS-reglur og JS hljóðlega. Til að vera alveg viss um
# að þetta gerist ekki er hér öll auð lína fjarlægð úr lokaskránni.
final_html = re.sub(r"\n[ \t]*\n+", "\n", final_html)

with open("bur-eining.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Wrote bur-eining.html,", len(final_html), "bytes  (þetta er skráin sem á að líma inn í WordPress)")
print("(Wrote _content.html,", len(content), "bytes — hjálparskjal, á ekki að nota beint)")
