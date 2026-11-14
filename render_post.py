#!/usr/bin/env python3
"""Rendert einen Beitrag je nach Typ in seine Folien."""
import json, os, sys
import cards
import render_carousel as rc

def slides_for(post, brand):
    b = cards.brand_for(brand, post.get("track", ""))
    t = post["type"]
    if t == "quiz":
        q, topic = post["question"], post["topic"]
        return [rc.slide_question(b, q, topic, 1, 3),
                rc.slide_answer(b, q, topic, 2, 3, post["explanation"]),
                cards.slide_merksatz(b, post["merksatz"], topic, 3, 3)]
    if t == "formel":
        return [cards.slide_formel(b, post, 1, 1)]
    if t == "verwechslung":
        return [cards.slide_verwechslung(b, post, 1, 1)]
    if t == "erklaerung":
        return [cards.slide_begriff(b, post, 1, 3),
                cards.slide_text(b, post, 2, 3, post.get("untertitel"), post["text"]),
                cards.slide_merksatz(b, post["merksatz"], post["topic"], 3, 3)]
    if t == "raetsel":
        return [cards.slide_raetsel(b, post, 1, 2),
                cards.slide_loesung(b, post, 2, 2)]
    raise ValueError("Unbekannter Typ: " + t)


def render(post, brandfile, outdir="docs/posts"):
    p = json.load(open(post, encoding="utf-8")) if isinstance(post, str) else post
    brand = json.load(open(brandfile, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for i, s in enumerate(slides_for(p, brand), 1):
        path = os.path.join(outdir, f"{p['id']}-{i}.jpg")
        s.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "docs/posts"):
        print(p)
