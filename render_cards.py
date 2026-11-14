#!/usr/bin/env python3
"""Weitere Kartentypen: Formel und Verwechslung. 1080x1350 JPEG."""
import json, os
from PIL import Image, ImageDraw
from render import font, hex2rgb, wrap, fit_font
from render_carousel import background, header, footer, rrect, W, H, MX, CW, TOP, BOT


def card_formel(brand, d_):
    img = background(brand)
    header(img, brand, d_["topic"], 1, 1)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])

    tf, ts = fit_font(d, d_["title"], "InterDisplay-Bold", CW, 58, 40)
    tl = wrap(d, d_["title"], tf, CW)
    ff, fs = fit_font(d, d_["formel"], "InterDisplay-Bold", CW - 72, 64, 36)
    rows = d_["teile"]
    rf = font("Inter-Medium", 32)
    rows_h = sum(max(70, len(wrap(d, r["text"], rf, CW - 240)) * 42 + 28) + 14 for r in rows)
    block = len(tl) * int(ts * 1.2) + 40 + 150 + 44 + rows_h
    y = TOP + max(0, (BOT - TOP - block) // 2)

    for ln in tl:
        d.text((MX, y), ln, font=tf, fill=txt + (255,), anchor="la")
        y += int(ts * 1.2)
    y += 40

    rrect(img, [MX, y, W - MX, y + 150], 24, acc + (34,), acc + (170,), 3)
    d.text((W / 2, y + 75), d_["formel"], font=ff, fill=txt + (255,), anchor="mm")
    y += 150 + 44

    for r in rows:
        rl = wrap(d, r["text"], rf, CW - 240)
        bh = max(70, len(rl) * 42 + 28)
        d.text((MX, y + bh / 2), r["label"], font=font("InterDisplay-SemiBold", 34),
               fill=acc + (255,), anchor="lm")
        ty = y + bh / 2 - (len(rl) - 1) * 21
        for ln in rl:
            d.text((MX + 200, ty), ln, font=rf, fill=dim + (255,), anchor="lm")
            ty += 42
        y += bh + 14

    footer(img, brand, brand["url"], highlight=True)
    return img


def card_verwechslung(brand, d_):
    img = background(brand)
    header(img, brand, d_["topic"], 1, 1)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    vio = hex2rgb(brand["secondary"])

    tf, ts = fit_font(d, d_["title"], "InterDisplay-Bold", CW, 58, 38)
    tl = wrap(d, d_["title"], tf, CW)
    colw = (CW - 28) // 2
    bf = font("Inter-Regular", 31)
    lh = 42
    la = wrap(d, d_["links"]["text"], bf, colw - 56)
    ra = wrap(d, d_["rechts"]["text"], bf, colw - 56)
    boxh = max(len(la), len(ra)) * lh + 150
    block = len(tl) * int(ts * 1.2) + 46 + boxh + 50
    y = TOP + max(0, (BOT - TOP - block) // 2)

    for ln in tl:
        d.text((MX, y), ln, font=tf, fill=txt + (255,), anchor="la")
        y += int(ts * 1.2)
    y += 46

    for i, (side, col, lines) in enumerate(
            [(d_["links"], acc, la), (d_["rechts"], vio, ra)]):
        x = MX + i * (colw + 28)
        rrect(img, [x, y, x + colw, y + boxh], 22, col + (26,), col + (150,), 2)
        d.text((x + 28, y + 46), side["name"], font=font("InterDisplay-Bold", 40),
               fill=col + (255,), anchor="lm")
        ty = y + 112
        for ln in lines:
            d.text((x + 28, ty), ln, font=bf, fill=dim + (255,), anchor="la")
            ty += lh
    y += boxh + 50
    if d_.get("merksatz"):
        mf = font("Inter-SemiBold", 34)
        for ln in wrap(d, d_["merksatz"], mf, CW):
            d.text((W / 2, y), ln, font=mf, fill=txt + (255,), anchor="ma")
            y += 46

    footer(img, brand, brand["url"], highlight=True)
    return img


if __name__ == "__main__":
    import sys
    brand = json.load(open("brand/wfw.json", encoding="utf-8"))
    os.makedirs("work/cards", exist_ok=True)

    formel = {"topic": "Rechnungswesen & Finanzen",
        "title": "Deckungsbeitrag",
        "formel": "Erlös − variable Kosten",
        "teile": [
            {"label": "Erlös", "text": "Was der Verkauf einbringt"},
            {"label": "variable K.", "text": "Kosten, die je Stück anfallen: Material, Akkordlohn, Energie"},
            {"label": "Ergebnis", "text": "Der Betrag, der zur Deckung der Fixkosten bleibt"},
        ]}
    card_formel(brand, formel).convert("RGB").save("work/cards/formel.jpg", "JPEG", quality=92)

    verw = {"topic": "Rechnungswesen & Finanzen",
        "title": "Aufwand ist nicht Kosten",
        "links": {"name": "Aufwand", "text": "Jeder Werteverzehr einer Periode, so wie ihn die Buchhaltung erfasst. Auch betriebsfremdes wie eine Spende."},
        "rechts": {"name": "Kosten", "text": "Nur der Werteverzehr, der dem eigentlichen Betriebszweck dient. Die Spende zählt hier nicht mit."},
        "merksatz": "Jede Kostenart ist Aufwand. Nicht jeder Aufwand ist Kosten."}
    card_verwechslung(brand, verw).convert("RGB").save("work/cards/verwechslung.jpg", "JPEG", quality=92)
    print("work/cards/formel.jpg\nwork/cards/verwechslung.jpg")
