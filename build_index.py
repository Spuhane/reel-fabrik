#!/usr/bin/env python3
"""Erzeugt docs/index.html - Freigabe- und Planungsuebersicht."""
import json, glob, html, os
from datetime import date, timedelta

FEIERTAGE = {(12, 24), (12, 25), (12, 26), (12, 31), (1, 1)}
START = date(2026, 11, 17)

posts = [json.load(open(f, encoding="utf-8")) for f in glob.glob("content/pool/q-*.json")]
car = sorted([p for p in posts if p["format"] == "carousel"], key=lambda p: p.get("order", 0))
ree = sorted([p for p in posts if p["format"] == "reel"], key=lambda p: p.get("order", 0))

posted = set()
sp = "state/posted.json"
if os.path.exists(sp):
    posted = {e["id"] for e in json.load(open(sp, encoding="utf-8")).get("posted", [])}

# Termine vergeben: Di Karussell, Do Reel, Feiertage ueberspringen
plan, d = {}, START
cq, rq = [p for p in car if p["id"] not in posted], [p for p in ree if p["id"] not in posted]
while cq or rq:
    if d.weekday() in (1, 3) and (d.month, d.day) not in FEIERTAGE:
        if d.weekday() == 1:
            p = cq.pop(0) if cq else (rq.pop(0) if rq else None)
        else:
            p = rq.pop(0) if rq else (cq.pop(0) if cq else None)
        if p: plan[p["id"]] = d
    d += timedelta(days=1)
    if d > START + timedelta(days=400): break

WD = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
alle = sorted(posts, key=lambda p: (plan.get(p["id"], date(2099, 1, 1)), p["id"]))

cards = []
for p in alle:
    if p["format"] == "reel":
        media = (f'<video controls preload="metadata" playsinline '
                 f'poster="" src="reels/{p["id"]}.mp4"></video>')
        badge = '<span class="fmt reel">Reel &middot; 17 s</span>'
    else:
        media = '<div class="slides">' + "".join(
            f'<a href="posts/{p["id"]}-{i}.jpg" target="_blank">'
            f'<img src="posts/{p["id"]}-{i}.jpg" alt="Folie {i}" loading="lazy"></a>'
            for i in (1, 2, 3)) + '</div>'
        badge = '<span class="fmt car">Karussell &middot; 3 Folien</span>'
    dt = plan.get(p["id"])
    when = (f'{WD[dt.weekday()]}, {dt.day:02d}.{dt.month:02d}.{dt.year}'
            if dt else 'bereits veröffentlicht')
    cards.append(f'''<article class="post">
  <header>
    <span class="when">{when}</span>{badge}
    <span class="topic">{html.escape(p["topic"])}</span>
    <span class="id">{p["id"]}</span>
  </header>
  {media}
  <details><summary>Caption anzeigen</summary>
    <p class="cap">{html.escape(p["caption"]).replace(chr(10), "<br>")}</p>
    <p class="tags">{" ".join(html.escape(t) for t in p["hashtags"])}</p></details>
</article>''')

letzter = max(plan.values()) if plan else None
schluss = (f'Der letzte geplante Beitrag läuft am {WD[letzter.weekday()]}, '
           f'{letzter.day:02d}.{letzter.month:02d}.{letzter.year}.' if letzter else '')

doc = f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Instagram-Plan &ndash; fachwirt_schulungen</title>
<style>
  :root {{ --bg:#0b0b0d; --card:#141418; --line:#26262c; --txt:#eceef2;
           --dim:#9aa0ac; --acc:#ff7a1a; --vio:#8b5cf6; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:28px 20px 80px; background:var(--bg); color:var(--txt);
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  h1 {{ font-size:30px; margin:0 0 6px; letter-spacing:-.02em; }}
  .lead {{ color:var(--dim); margin:0 0 10px; }}
  .stats {{ display:flex; gap:10px; flex-wrap:wrap; margin:18px 0 34px; }}
  .stat {{ background:var(--card); border:1px solid var(--line); border-radius:12px;
           padding:12px 18px; }}
  .stat b {{ display:block; font-size:24px; }}
  .stat span {{ color:var(--dim); font-size:13px; }}
  .post {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
           padding:16px; margin-bottom:18px; }}
  .post header {{ display:flex; gap:10px; align-items:center; margin-bottom:12px;
                  font-size:13px; color:var(--dim); flex-wrap:wrap; }}
  .when {{ color:var(--txt); font-weight:600; }}
  .fmt {{ padding:2px 10px; border-radius:20px; font-size:12px; }}
  .fmt.reel {{ border:1px solid var(--vio); color:#b79cff; }}
  .fmt.car {{ border:1px solid var(--acc); color:var(--acc); }}
  .topic {{ }}
  .id {{ margin-left:auto; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .slides {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }}
  .slides img {{ width:100%; border-radius:10px; display:block; border:1px solid var(--line); }}
  video {{ width:100%; max-width:330px; border-radius:12px; display:block;
           border:1px solid var(--line); background:#000; }}
  details {{ margin-top:12px; }}
  summary {{ cursor:pointer; color:var(--dim); font-size:14px; }}
  .tags {{ color:var(--acc); font-size:14px; word-spacing:4px; }}
  @media (max-width:640px) {{ .slides {{ grid-template-columns:1fr; }} }}
</style></head><body><div class="wrap">
<h1>Instagram-Plan</h1>
<p class="lead">@fachwirt_schulungen &middot; dienstags Karussell, donnerstags Reel, jeweils 19:41 Uhr.
Heiligabend, Weihnachten und Silvester werden übersprungen. {schluss}</p>
<div class="stats">
  <div class="stat"><b>{len(alle)}</b><span>Beiträge gesamt</span></div>
  <div class="stat"><b>{len(car)}</b><span>Karussells</span></div>
  <div class="stat"><b>{len(ree)}</b><span>Reels</span></div>
</div>
{"".join(cards)}
</div></body></html>'''

os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w", encoding="utf-8").write(doc)
print(f"index.html: {len(alle)} Beitraege, letzter Termin {letzter}")
