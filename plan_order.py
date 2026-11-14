#!/usr/bin/env python3
"""Vergibt die Reihenfolge so, dass die Inhaltstypen einander abwechseln.

Statt reihum durch die Toepfe zu gehen (dann klumpt der groesste am Ende),
bekommt jeder Beitrag eine relative Position innerhalb seines Topfes.
Nach dieser Position wird sortiert, dadurch verteilt sich jeder Typ
gleichmaessig ueber die gesamte Laufzeit.
"""
import json, glob, collections

posts = [json.load(open(f, encoding="utf-8")) for f in glob.glob("content/pool/*.json")]

# Altlast: im ersten Entwurf stand im Feld "type" das Format.
for p in posts:
    if p["type"] in ("carousel", "reel", "single"):
        p["type"] = "quiz"


def bucket(p):
    if p["type"] == "quiz":
        return "quiz-reel" if p["format"] == "reel" else "quiz-karussell"
    return p["type"]


buckets = collections.defaultdict(list)
for p in posts:
    buckets[bucket(p)].append(p)

# Themen innerhalb eines Topfes streuen
for k, v in buckets.items():
    by_topic = collections.defaultdict(list)
    for p in v:
        by_topic[p["topic"]].append(p)
    mixed = []
    while any(by_topic.values()):
        for t in sorted(by_topic):
            if by_topic[t]:
                mixed.append(by_topic[t].pop(0))
    buckets[k] = mixed

# jeder Beitrag bekommt seine relative Lage im Topf, danach wird sortiert
keyed = []
for k, v in buckets.items():
    for i, p in enumerate(v):
        keyed.append(((i + 0.5) / len(v), k, p))
keyed.sort(key=lambda x: (x[0], x[1]))

order = [p for _, _, p in keyed]
for i, p in enumerate(order, 1):
    p["order"] = i
    json.dump(p, open(f"content/pool/{p['id']}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

print(f"Reihenfolge vergeben: {len(order)} Beitraege")
print("Verteilung:", {k: len(v) for k, v in sorted(buckets.items())}, "\n")
letzter, wdh = None, 0
for p in order:
    b = bucket(p)
    mark = ""
    if b == letzter:
        wdh += 1
        mark = "  <- Wiederholung"
    letzter = b
    print(f"  {p['order']:3d}. {b:16s} {p['id']}{mark}")
print(f"\nGleiche Typen hintereinander: {wdh}")
