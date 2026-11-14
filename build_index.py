#!/usr/bin/env python3
"""Erzeugt docs/index.html - Freigabe-Uebersicht aller Posts im Pool."""
import json, glob, html, os

posts = []
for f in sorted(glob.glob("content/pool/q-*.json")):
    posts.append(json.load(open(f, encoding="utf-8")))

by_topic = {}
for p in posts:
    by_topic.setdefault(p["topic"], []).append(p)

cards = []
for topic in sorted(by_topic):
    cards.append(f'<h2 class="topic">{html.escape(topic)}</h2>')
    for p in by_topic[topic]:
        slides = "".join(
            f'<a href="posts/{p["id"]}-{i}.jpg" target="_blank">'
            f'<img src="posts/{p["id"]}-{i}.jpg" alt="Folie {i}" loading="lazy"></a>'
            for i in (1, 2, 3))
        tags = " ".join(html.escape(t) for t in p["hashtags"])
        cap = html.escape(p["caption"]).replace("\n", "<br>")
        cards.append(f'''<article class="post" id="{p["id"]}">
  <header><span class="id">{p["id"]}</span>
  <span class="src">Frage {html.escape(p["source_question_id"])}</span>
  <span class="status">{html.escape(p["status"])}</span></header>
  <div class="slides">{slides}</div>
  <details><summary>Caption anzeigen</summary>
    <p class="cap">{cap}</p><p class="tags">{tags}</p></details>
</article>''')

doc = f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Freigabe &ndash; Instagram-Posts</title>
<style>
  :root {{ --bg:#0b0b0d; --card:#141418; --line:#26262c; --txt:#eceef2;
           --dim:#9aa0ac; --acc:#ff7a1a; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:28px 20px 80px; background:var(--bg); color:var(--txt);
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  h1 {{ font-size:30px; margin:0 0 6px; letter-spacing:-.02em; }}
  .lead {{ color:var(--dim); margin:0 0 34px; }}
  .topic {{ font-size:15px; text-transform:uppercase; letter-spacing:.09em;
            color:var(--acc); margin:40px 0 14px; border-top:1px solid var(--line);
            padding-top:18px; }}
  .post {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
           padding:16px; margin-bottom:18px; }}
  .post header {{ display:flex; gap:12px; align-items:center; margin-bottom:12px;
                  font-size:13px; color:var(--dim); flex-wrap:wrap; }}
  .id {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--txt); }}
  .status {{ margin-left:auto; border:1px solid var(--acc); color:var(--acc);
             padding:2px 10px; border-radius:20px; font-size:12px; }}
  .slides {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }}
  .slides img {{ width:100%; border-radius:10px; display:block; border:1px solid var(--line); }}
  details {{ margin-top:12px; }}
  summary {{ cursor:pointer; color:var(--dim); font-size:14px; }}
  .cap {{ white-space:normal; color:var(--txt); }}
  .tags {{ color:var(--acc); font-size:14px; word-spacing:4px; }}
  @media (max-width:640px) {{ .slides {{ grid-template-columns:1fr; }} }}
</style></head><body><div class="wrap">
<h1>Freigabe: Instagram-Posts</h1>
<p class="lead">{len(posts)} Karussells aus dem Fragenkatalog, {len(by_topic)} Themengebiete.
Jedes Bild zum Vergrößern anklicken. Alles steht auf Entwurf &ndash; es geht nichts raus ohne deine Freigabe.</p>
{"".join(cards)}
</div></body></html>'''

os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w", encoding="utf-8").write(doc)
print(f"docs/index.html geschrieben: {len(posts)} Posts, {len(by_topic)} Themen")
