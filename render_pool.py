#!/usr/bin/env python3
import json, glob, traceback
import render_post
ok = err = 0
for f in sorted(glob.glob("content/pool/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    if p.get("format") == "reel":
        continue
    try:
        n = len(render_post.render(p, "brand/wfw.json", "docs/posts"))
        print(f"  {p['id']:28s} {p['type']:14s} {n} Folien")
        ok += 1
    except Exception as e:
        print(f"  FEHLER {p['id']}: {e}")
        traceback.print_exc()
        err += 1
print(f"\nGerendert: {ok}   Fehler: {err}")
