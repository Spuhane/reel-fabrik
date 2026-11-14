#!/usr/bin/env python3
"""Rendert alle Karussell-Posts aus content/pool/."""
import json, glob, os, sys
import render_carousel as rc

outdir = sys.argv[1] if len(sys.argv) > 1 else "docs/posts"
os.makedirs(outdir, exist_ok=True)
made = 0
for f in sorted(glob.glob("content/pool/q-*.json")):
    post = json.load(open(f, encoding="utf-8"))
    brand = json.load(open(f"brand/{post['brand']}.json", encoding="utf-8"))
    q = post["question"]
    slides = [
        rc.slide_question(brand, q, post["topic"], 1, 3),
        rc.slide_answer(brand, q, post["topic"], 2, 3, post["explanation"]),
        rc.slide_cta(brand, "1.393", 3, 3),
    ]
    for i, s in enumerate(slides, 1):
        p = os.path.join(outdir, f"{post['id']}-{i}.jpg")
        s.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    made += 1
    print(f"  {post['id']}  {post['topic']}")
print("Karussells gerendert:", made)
