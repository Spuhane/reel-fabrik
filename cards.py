#!/usr/bin/env python3
"""Alle Kartentypen im gemeinsamen Gestaltungssystem. 1080x1350 JPEG."""
import json, os
from PIL import Image, ImageDraw
from render import font, hex2rgb, wrap, fit_font
from render_carousel import (background, header, footer, rrect, ellipse_a,
                             W, H, MX, CW, TOP, BOT)


def brand_for(brand, track):
    """Farben bleiben ueber alle Beitraege gleich.

    Eine Akzentfarbe je Handlungsbereich war erwogen und verworfen: Sie
    faerbte auch das Logo um, mal orange mal violett. Die Abwechslung
    kommt aus den fuenf Inhaltstypen, nicht aus der Farbe.
    (Stefan: "Layout bleibt", 14.11.2026)
    """
    return brand


def _title(d, img, text, y, size=58, color=None, brand=None):
    f, s = fit_font(d, text, "InterDisplay-Bold", CW, size, 38)
    lines = wrap(d, text, f, CW)
    col = color or hex2rgb(brand["text"])
    for ln in lines:
        d.text((MX, y), ln, font=f, fill=col + (255,), anchor="la")
        y += int(s * 1.2)
    return y


def _h_title(d, text, size=58):
    f, s = fit_font(d, text, "InterDisplay-Bold", CW, size, 38)
    return len(wrap(d, text, f, CW)) * int(s * 1.2)


# ---------- Folie: Merksatz (ersetzt die alte Werbefolie) ----------
def slide_merksatz(brand, text, topic, page, pages, kicker="Merk dir das"):
    img = background(brand)
    header(img, brand, topic, page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    f, s = fit_font(d, text, "InterDisplay-Bold", CW, 56, 36)
    lines = wrap(d, text, f, CW)
    block = 70 + len(lines) * int(s * 1.26)
    y = TOP + max(0, (BOT - TOP - block) // 2)
    d.text((MX, y), kicker, font=font("Inter-Medium", 32), fill=acc + (255,), anchor="la")
    y += 70
    for ln in lines:
        d.text((MX, y), ln, font=f, fill=txt + (255,), anchor="la")
        y += int(s * 1.26)
    footer(img, brand, brand["url"], highlight=True)
    return img


# ---------- Typ: Formel ----------
def slide_formel(brand, p, page, pages):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    rf = font("Inter-Medium", 32)

    # Label-Spalte richtet sich nach dem laengsten Label, statt fest zu sein.
    # Vorher lief "Kapitalumschlag" in den Erklaerungstext hinein.
    size = 34
    lf = font("InterDisplay-SemiBold", size)
    widest = lambda f: max(d.textlength(r["label"], font=f) for r in p["teile"])
    while size > 24 and widest(lf) > CW * 0.40:
        size -= 2
        lf = font("InterDisplay-SemiBold", size)
    colw = int(widest(lf)) + 34
    textw = CW - colw

    rows_h = sum(max(70, len(wrap(d, r["text"], rf, textw)) * 42 + 28) + 14 for r in p["teile"])
    block = _h_title(d, p["title"]) + 40 + 150 + 44 + rows_h
    y = TOP + max(0, (BOT - TOP - block) // 2)
    y = _title(d, img, p["title"], y, brand=brand)
    y += 40
    ff, _ = fit_font(d, p["formel"], "InterDisplay-Bold", CW - 72, 64, 34)
    rrect(img, [MX, y, W - MX, y + 150], 24, acc + (34,), acc + (170,), 3)
    d.text((W / 2, y + 75), p["formel"], font=ff, fill=txt + (255,), anchor="mm")
    y += 194
    for r in p["teile"]:
        rl = wrap(d, r["text"], rf, textw)
        bh = max(70, len(rl) * 42 + 28)
        d.text((MX, y + bh / 2), r["label"], font=lf, fill=acc + (255,), anchor="lm")
        ty = y + bh / 2 - (len(rl) - 1) * 21
        for ln in rl:
            d.text((MX + colw, ty), ln, font=rf, fill=dim + (255,), anchor="lm")
            ty += 42
        y += bh + 14
    footer(img, brand, brand["url"], highlight=True)
    return img


# ---------- Typ: Verwechslung ----------
def slide_verwechslung(brand, p, page, pages):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    vio = hex2rgb(brand["secondary"])
    colw = (CW - 28) // 2
    bf = font("Inter-Regular", 31)
    la = wrap(d, p["links"]["text"], bf, colw - 56)
    ra = wrap(d, p["rechts"]["text"], bf, colw - 56)
    boxh = max(len(la), len(ra)) * 42 + 150
    mh = len(wrap(d, p.get("merksatz", ""), font("Inter-SemiBold", 34), CW)) * 46 if p.get("merksatz") else 0
    block = _h_title(d, p["title"]) + 46 + boxh + (50 + mh if mh else 0)
    y = TOP + max(0, (BOT - TOP - block) // 2)
    y = _title(d, img, p["title"], y, brand=brand)
    y += 46
    for i, (side, col, lines) in enumerate([(p["links"], acc, la), (p["rechts"], vio, ra)]):
        x = MX + i * (colw + 28)
        rrect(img, [x, y, x + colw, y + boxh], 22, col + (26,), col + (150,), 2)
        d.text((x + 28, y + 46), side["name"], font=font("InterDisplay-Bold", 40),
               fill=col + (255,), anchor="lm")
        ty = y + 112
        for ln in lines:
            d.text((x + 28, ty), ln, font=bf, fill=dim + (255,), anchor="la")
            ty += 42
    y += boxh + 50
    if p.get("merksatz"):
        mf = font("Inter-SemiBold", 34)
        for ln in wrap(d, p["merksatz"], mf, CW):
            d.text((W / 2, y), ln, font=mf, fill=txt + (255,), anchor="ma")
            y += 46
    footer(img, brand, brand["url"], highlight=True)
    return img


# ---------- Typ: Erklaerung ----------
def slide_begriff(brand, p, page, pages, hint="Was dahintersteckt  →"):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    kf = font("Inter-Medium", 34)
    sub = p.get("kicker", "Kurz erklärt")
    tf, ts = fit_font(d, p["begriff"], "InterDisplay-Bold", CW, 92, 48)
    tl = wrap(d, p["begriff"], tf, CW)
    block = 60 + len(tl) * int(ts * 1.16)
    y = TOP + max(0, (BOT - TOP - block) // 2) - 40
    d.text((MX, y), sub, font=kf, fill=acc + (255,), anchor="la")
    y += 60
    for ln in tl:
        d.text((MX, y), ln, font=tf, fill=txt + (255,), anchor="la")
        y += int(ts * 1.16)
    footer(img, brand, hint)
    return img


def slide_text(brand, p, page, pages, title, body):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"])
    bf = font("Inter-Regular", 35)
    bl = wrap(d, body, bf, CW)
    block = (_h_title(d, title, 50) + 36 if title else 0) + len(bl) * 50
    y = TOP + max(0, (BOT - TOP - block) // 2)
    if title:
        y = _title(d, img, title, y, size=50, brand=brand)
        y += 36
    for ln in bl:
        d.text((MX, y), ln, font=bf, fill=dim + (255,), anchor="la")
        y += 50
    footer(img, brand, brand["url"], highlight=True)
    return img


# ---------- Typ: Raetsel ----------
def slide_raetsel(brand, p, page, pages, hint="Lösung auf der nächsten Folie  →"):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    gf = font("Inter-Medium", 34)
    rows = p["gegeben"]
    rows_h = sum(max(66, len(wrap(d, r["wert"], gf, CW - 300)) * 42 + 24) + 12 for r in rows)
    ff, fs = fit_font(d, p["frage"], "InterDisplay-Bold", CW, 52, 34)
    fl = wrap(d, p["frage"], ff, CW)
    block = 64 + rows_h + 50 + len(fl) * int(fs * 1.2)
    y = TOP + max(0, (BOT - TOP - block) // 2)
    d.text((MX, y), "Rechne mit", font=font("Inter-Medium", 32), fill=acc + (255,), anchor="la")
    y += 64
    for r in rows:
        rl = wrap(d, r["wert"], gf, CW - 300)
        bh = max(66, len(rl) * 42 + 24)
        rrect(img, [MX, y, W - MX, y + bh], 18, (255, 255, 255, 14), (255, 255, 255, 44), 2)
        d.text((MX + 28, y + bh / 2), r["label"], font=font("Inter-SemiBold", 32),
               fill=dim + (255,), anchor="lm")
        d.text((W - MX - 28, y + bh / 2), r["wert"], font=font("InterDisplay-SemiBold", 36),
               fill=txt + (255,), anchor="rm")
        y += bh + 12
    y += 50
    for ln in fl:
        d.text((MX, y), ln, font=ff, fill=txt + (255,), anchor="la")
        y += int(fs * 1.2)
    footer(img, brand, hint)
    return img


def slide_loesung(brand, p, page, pages):
    img = background(brand)
    header(img, brand, p["topic"], page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    ef = font("Inter-Regular", 34)
    el = wrap(d, p["rechenweg"], ef, CW)
    rf, rs = fit_font(d, p["ergebnis"], "InterDisplay-Bold", CW - 72, 64, 36)
    block = 58 + 140 + 44 + len(el) * 46
    y = TOP + max(0, (BOT - TOP - block) // 2)
    d.text((MX, y), "Ergebnis", font=font("Inter-Medium", 34), fill=dim + (255,), anchor="la")
    y += 58
    rrect(img, [MX, y, W - MX, y + 140], 24, acc + (42,), acc + (210,), 3)
    d.text((W / 2, y + 70), p["ergebnis"], font=rf, fill=txt + (255,), anchor="mm")
    y += 184
    for ln in el:
        d.text((MX, y), ln, font=ef, fill=dim + (255,), anchor="la")
        y += 46
    footer(img, brand, brand["url"], highlight=True)
    return img
