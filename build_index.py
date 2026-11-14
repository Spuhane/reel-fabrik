#!/usr/bin/env python3
"""Erzeugt docs/index.html - Redaktionsplan und Freigabeuebersicht."""
import json, glob, html, os
from datetime import date, timedelta

FEIERTAGE = {(12, 24), (12, 25), (12, 26), (12, 31), (1, 1)}
START = date(2026, 11, 17)
WD = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

LABEL = {"quiz": "Quiz", "formel": "Formel", "verwechslung": "Verwechslung",
         "erklaerung": "Erklärung", "raetsel": "Rätsel"}

posts = sorted((json.load(open(f, encoding="utf-8"))
                for f in glob.glob("content/pool/*.json")),
               key=lambda p: p.get("order", 999))

posted = set()
if os.path.exists("state/posted.json"):
    posted = {e["id"] for e in json.load(open("state/posted.json", encoding="utf-8")).get("posted", [])}

# Termine: Di und Do, Feiertage ausgelassen, in der Reihenfolge von "order"
plan, d, i = {}, START, 0
offen = [p for p in posts if p["id"] not in posted]
while i < len(offen):
    if d.weekday() in (1, 3) and (d.month, d.day) not in FEIERTAGE:
        plan[offen[i]["id"]] = d
        i += 1
    d += timedelta(days=1)

typen = {}
for p in posts:
    typen[p["type"]] = typen.get(p["type"], 0) + 1

cards = []
for p in posts:
    pid, t = p["id"], p["type"]
    if p["format"] == "reel":
        media = f'<video controls preload="metadata" playsinline src="reels/{pid}.mp4"></video>'
        fmt = "Reel · 17 s"
    else:
        n = len(p.get("images", []))
        media = '<div class="slides s%d">%s</div>' % (n, "".join(
            f'<a href="posts/{pid}-{k}.jpg" target="_blank">'
            f'<img src="posts/{pid}-{k}.jpg" alt="Folie {k}" loading="lazy"></a>'
            for k in range(1, n + 1)))
        fmt = "Einzelbild" if n == 1 else f"Karussell · {n} Folien"
    dt = plan.get(pid)
    when = (f'{WD[dt.weekday()]}, {dt.day:02d}.{dt.month:02d}.{dt.year}'
            if dt else 'veröffentlicht')
    cards.append(f'''<article class="post">
  <header>
    <span class="num">{p.get("order","")}</span>
    <span class="when">{when}</span>
    <span class="typ t-{t}">{LABEL.get(t, t)}</span>
    <span class="fmt">{fmt}</span>
    <span class="topic">{html.escape(p["topic"])}</span>
    <span class="id">{pid}</span>
  </header>
  {media}
  <details><summary>Caption anzeigen</summary>
    <p class="cap">{html.escape(p["caption"]).replace(chr(10), "<br>")}</p>
    <p class="tags">{" ".join(html.escape(x) for x in p["hashtags"])}</p></details>
</article>''')

letzter = max(plan.values()) if plan else None
schluss = (f'Der letzte geplante Beitrag läuft am {WD[letzter.weekday()]}, '
           f'{letzter.day:02d}.{letzter.month:02d}.{letzter.year}.' if letzter else '')
stats = "".join(f'<div class="stat"><b>{v}</b><span>{LABEL.get(k,k)}</span></div>'
                for k, v in sorted(typen.items(), key=lambda x: -x[1]))

doc = f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Redaktionsplan &ndash; fachwirt_schulungen</title>
<style>
  :root {{ --bg:#0b0b0d; --card:#141418; --line:#26262c; --txt:#eceef2;
           --dim:#9aa0ac; --acc:#ff7a1a; --vio:#8b5cf6; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:28px 20px 80px; background:var(--bg); color:var(--txt);
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  h1 {{ font-size:30px; margin:0 0 6px; letter-spacing:-.02em; }}
  .lead {{ color:var(--dim); margin:0 0 18px; }}
  .stats {{ display:flex; gap:10px; flex-wrap:wrap; margin:0 0 34px; }}
  .stat {{ background:var(--card); border:1px solid var(--line); border-radius:12px;
           padding:10px 16px; }}
  .stat b {{ display:block; font-size:22px; }}
  .stat span {{ color:var(--dim); font-size:13px; }}
  .post {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
           padding:16px; margin-bottom:18px; }}
  .post header {{ display:flex; gap:10px; align-items:center; margin-bottom:12px;
                  font-size:13px; color:var(--dim); flex-wrap:wrap; }}
  .num {{ color:var(--dim); font-variant-numeric:tabular-nums; min-width:26px; }}
  .when {{ color:var(--txt); font-weight:600; }}
  .typ {{ padding:2px 10px; border-radius:20px; font-size:12px;
          border:1px solid var(--acc); color:var(--acc); }}
  .typ.t-quiz {{ border-color:var(--vio); color:#b79cff; }}
  .typ.t-raetsel {{ border-color:#4ade80; color:#4ade80; }}
  .typ.t-formel {{ border-color:#60a5fa; color:#60a5fa; }}
  .id {{ margin-left:auto; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .slides {{ display:grid; gap:10px; }}
  .slides.s1 {{ grid-template-columns:minmax(0,340px); }}
  .slides.s2 {{ grid-template-columns:repeat(2,1fr); }}
  .slides.s3 {{ grid-template-columns:repeat(3,1fr); }}
  .slides img {{ width:100%; border-radius:10px; display:block; border:1px solid var(--line); }}
  video {{ width:100%; max-width:330px; border-radius:12px; display:block;
           border:1px solid var(--line); background:#000; }}
  details {{ margin-top:12px; }}
  summary {{ cursor:pointer; color:var(--dim); font-size:14px; }}
  .tags {{ color:var(--acc); font-size:14px; word-spacing:4px; }}
  @media (max-width:640px) {{ .slides {{ grid-template-columns:1fr !important; }} }}
</style></head><body><div class="wrap">
<h1>Redaktionsplan</h1>
<p class="lead">@fachwirt_schulungen &middot; dienstags und donnerstags 19:41 Uhr.
Die Inhaltstypen wechseln einander ab, Feiertage werden übersprungen. {schluss}</p>
<div class="stats"><div class="stat"><b>{len(posts)}</b><span>Beiträge</span></div>{stats}</div>
{"".join(cards)}
</div></body></html>'''

os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w", encoding="utf-8").write(doc)
print(f"index.html: {len(posts)} Beitraege, Typen {typen}, letzter Termin {letzter}")
