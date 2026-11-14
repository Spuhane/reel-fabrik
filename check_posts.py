#!/usr/bin/env python3
"""Prueft jeden Post rechnerisch auf Ueberlauf und abgeschnittene Erklaerungen."""
import json, glob
from PIL import Image, ImageDraw
import render_carousel as rc
from render import font, wrap, fit_font

probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
problems = []
for f in sorted(glob.glob("content/pool/q-*.json")):
    p = json.load(open(f, encoding="utf-8"))
    q = p["question"]

    # Folie 1
    qt = q.get("social_question") or q["question"]
    qf, qs = fit_font(probe, qt, "InterDisplay-Bold", rc.CW, 62, 40)
    qlines = wrap(probe, qt, qf, rc.CW)
    of = font("Inter-Medium", 34)
    boxes = [max(84, len(wrap(probe, o, of, rc.CW - 104)) * 44 + 40) for o in q["options"]]
    block1 = len(qlines) * int(qs * 1.22) + 44 + sum(b + 18 for b in boxes) - 18
    avail = rc.BOT - rc.TOP
    if block1 > avail:
        problems.append((p["id"], "Folie 1", f"Block {block1}px > verfuegbar {avail}px"))

    # Folie 2
    correct = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
    af, asz = fit_font(probe, max((q["options"][c] for c in correct), key=len),
                       "InterDisplay-Bold", rc.CW - 104, 50, 32)
    elines = wrap(probe, p["explanation"], font("Inter-Regular", 34), rc.CW)
    bh = sum(max(96, len(wrap(probe, q["options"][c], af, rc.CW - 104)) * int(asz * 1.2) + 48) + 16
             for c in correct)
    block2 = 58 + bh + 40 + len(elines) * 48
    if block2 > avail:
        problems.append((p["id"], "Folie 2", f"Block {block2}px > verfuegbar {avail}px ({len(elines)} Zeilen Erklaerung)"))

    # Caption-Laenge (Instagram: 2200 Zeichen)
    full = p["caption"] + "\n\n" + " ".join(p["hashtags"])
    if len(full) > 2200:
        problems.append((p["id"], "Caption", f"{len(full)} Zeichen > 2200"))
    if len(p["hashtags"]) > 30:
        problems.append((p["id"], "Hashtags", f"{len(p['hashtags'])} > 30"))
    # jeder Hashtag mit Raute?
    for h in p["hashtags"]:
        if not h.startswith("#"):
            problems.append((p["id"], "Hashtag ohne Raute", h))

print("Posts geprueft:", len(glob.glob("content/pool/q-*.json")))
if problems:
    print("\nBefunde:")
    for pid, where, what in problems:
        print(f"  {pid:14s} {where:22s} {what}")
else:
    print("Keine Ueberlaeufe, keine Caption-Verstoesse.")
