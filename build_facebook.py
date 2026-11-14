#!/usr/bin/env python3
"""Erzeugt je Beitrag die Facebook-Fassung.

Facebook nimmt ueber die Schnittstelle weder Karussells noch Videos, dafuer
sehr lange Texte. Also: ein Bild als Aufhaenger, und was auf den weiteren
Folien stand, wandert vollstaendig in den Text. Keine beschnittene Kopie,
sondern eine Fassung fuer ein Medium, in dem gelesen wird.
"""
import json, glob

CTA = "Über 1.300 Prüfungsfragen mit Erklärung zu jeder Antwort: wirtschaftsfachwirt-pro.de"
# Auf Facebook wirken wenige Hashtags besser als viele.
TAGS = ["#wirtschaftsfachwirt", "#ihkprüfung", "#weiterbildung", "#aufstiegsfortbildung"]


def caption(p):
    t = p["type"]
    teile = []

    if t == "quiz":
        q = p["question"]
        teile.append(q.get("social_question") or q["question"])
        teile.append("\n".join(f"{'ABCD'[i]}) {o}" for i, o in enumerate(q["options"])))
        korrekt = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
        loesung = ", ".join(f"{'ABCD'[c]}) {q['options'][c]}" for c in korrekt)
        teile.append(f"Richtig ist {loesung}.")
        teile.append(p["explanation"])
        if p.get("merksatz"):
            teile.append(p["merksatz"])

    elif t == "formel":
        teile.append(f"{p['title']} = {p['formel']}")
        teile.append("\n".join(f"{r['label']}: {r['text']}" for r in p["teile"]))
        teile.append(p["caption"])

    elif t == "verwechslung":
        teile.append(p["title"])
        teile.append(f"{p['links']['name']}: {p['links']['text']}")
        teile.append(f"{p['rechts']['name']}: {p['rechts']['text']}")
        if p.get("merksatz"):
            teile.append(p["merksatz"])

    elif t == "erklaerung":
        teile.append(f"{p['begriff']} – {p.get('untertitel','')}".strip(" –"))
        teile.append(p["text"])
        teile.append(p["merksatz"])

    elif t == "raetsel":
        teile.append("Rechenaufgabe zum Mitrechnen:")
        teile.append("\n".join(f"{g['label']}: {g['wert']}" for g in p["gegeben"]))
        teile.append(p["frage"])
        teile.append(f"Ergebnis: {p['ergebnis']}")
        teile.append(p["rechenweg"])

    teile.append(CTA)
    teile.append(" ".join(TAGS))
    return "\n\n".join(x for x in teile if x)


def bild(p):
    """Facebook bekommt immer eine Folie: den Aufhaenger."""
    if p["format"] == "reel":
        # Reels haben keine JPEGs; die Frageseite wird dafuer gerendert.
        return f"https://spuhane.github.io/reel-fabrik/posts/{p['id']}-fb.jpg"
    return p["images"][0]


if __name__ == "__main__":
    n = 0
    laengen = []
    for f in sorted(glob.glob("content/pool/*.json")):
        p = json.load(open(f, encoding="utf-8"))
        c = caption(p)
        p["facebook"] = {"image": bild(p), "caption": c}
        laengen.append((len(c), p["id"]))
        json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        n += 1
    laengen.sort(reverse=True)
    print(f"Facebook-Fassungen erzeugt: {n}")
    print(f"Laengster Text: {laengen[0][0]} Zeichen ({laengen[0][1]}), Limit 63206")
    print(f"Kuerzester:     {laengen[-1][0]} Zeichen ({laengen[-1][1]})")
