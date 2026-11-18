#!/usr/bin/env python3
"""Eigene Facebook-Bilder: eine Folie, kein Seitenzaehler, Hinweis auf den Text.

Facebook bekommt ueber die Schnittstelle nur ein Bild je Beitrag. Die
Aufloesung steht dort im Beitragstext. Ein Bild mit "1/3" und "Antwort auf
der naechsten Folie" fuehrt ins Leere (Stefan, 18.11.2026).
"""
import json, glob
import render_carousel as rc
import cards

HINT = "Auflösung im Text darunter  ↓"

brand = json.load(open("brand/wfw.json", encoding="utf-8"))
n = 0
for f in sorted(glob.glob("content/pool/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    t = p["type"]
    if t == "quiz":
        img = rc.slide_question(brand, p["question"], p["topic"], 1, 1, hint=HINT)
    elif t == "raetsel":
        img = cards.slide_raetsel(brand, p, 1, 1, hint="Lösung im Text darunter  ↓")
    elif t == "erklaerung":
        img = cards.slide_begriff(brand, p, 1, 1, hint="Erklärung im Text darunter  ↓")
    elif t == "formel":
        img = cards.slide_formel(brand, p, 1, 1)
    elif t == "verwechslung":
        img = cards.slide_verwechslung(brand, p, 1, 1)
    else:
        continue
    img.convert("RGB").save(f"docs/posts/{p['id']}-fb.jpg", "JPEG", quality=90, optimize=True)
    p.setdefault("facebook", {})["image"] = \
        f"https://spuhane.github.io/reel-fabrik/posts/{p['id']}-fb.jpg"
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    n += 1
print("Facebook-Bilder gerendert:", n)
