#!/usr/bin/env python3
"""Karussell-Renderer: Pruefungsfrage -> JPEG-Folien 1080x1350 fuer Instagram."""
import json, math, os, sys, argparse
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from render import font, hex2rgb, wrap, fit_font

W, H = 1080, 1350            # 4:5, von Instagram fuer Karussells erlaubt
MX = 88                      # Seitenrand
TOP, BOT = 300, 1200         # vertikaler Satzspiegel
CW = W - 2 * MX


def rrect(img, box, radius, fill=None, outline=None, width=2):
    """Halbtransparente Flaeche echt mischen - ImageDraw ueberschreibt sonst."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill,
                                            outline=outline, width=width)
    img.alpha_composite(layer)


def ellipse_a(img, box, fill):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(box, fill=fill)
    img.alpha_composite(layer)


def background(brand):
    bw, bh = W, H
    arr = np.full((bh, bw, 3), hex2rgb(brand["bg"]), dtype=np.float32)
    yy, xx = np.mgrid[0:bh, 0:bw]
    for cx, cy, r, col, s in [
        (bw * 0.85, bh * 0.10, bw * 0.85, hex2rgb(brand["accent"]), 0.26),
        (bw * 0.10, bh * 0.92, bw * 0.80, hex2rgb(brand["secondary"]), 0.18),
    ]:
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        a = (np.clip(1 - d, 0, 1) ** 2.2 * s)[:, :, None]
        layer = np.zeros_like(arr)
        for i, c in enumerate(col):
            layer[:, :, i] = c
        arr = arr * (1 - a) + layer * a
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img.filter(ImageFilter.GaussianBlur(55)).convert("RGBA")


def header(img, brand, topic, page, pages):
    d = ImageDraw.Draw(img)
    acc, txt, dim = hex2rgb(brand["accent"]), hex2rgb(brand["text"]), hex2rgb(brand["text_dim"])
    # Logo-Mark + Markenname, gerade
    d.ellipse([MX, 72, MX + 68, 140], fill=hex2rgb(brand["secondary"]) + (255,))
    d.text((MX + 34, 107), brand["mark"], font=font("InterDisplay-Bold", 38),
           fill=(255, 255, 255, 255), anchor="mm")
    d.text((MX + 88, 106), brand["name"], font=font("InterDisplay-SemiBold", 34),
           fill=txt + (255,), anchor="lm")
    # Seitenzaehler
    if pages and pages > 1:
      d.text((W - MX, 106), f"{page}/{pages}", font=font("Inter-Medium", 30),
           fill=dim + (255,), anchor="rm")
    # Themen-Chip
    if topic:
        f = font("Inter-SemiBold", 26)
        tw = d.textlength(topic, font=f)
        rrect(img, [MX, 178, MX + tw + 48, 236], 29, acc + (34,), acc + (120,), 2)
        d.text((MX + 24, 208), topic, font=f, fill=acc + (255,), anchor="lm")


def footer(img, brand, text, highlight=False):
    d = ImageDraw.Draw(img)
    f = font("Inter-SemiBold", 30)
    tw = d.textlength(text, font=f)
    if highlight:
        pw, ph = int(tw) + 72, 74
        rrect(img, [(W - pw) // 2, H - 134, (W + pw) // 2, H - 134 + ph], 37,
              hex2rgb(brand["accent"]) + (255,))
        d.text((W / 2, H - 97), text, font=f, fill=(10, 10, 12, 255), anchor="mm")
    else:
        d.text((W / 2, H - 97), text, font=f,
               fill=hex2rgb(brand["text_dim"]) + (255,), anchor="mm")


def slide_question(brand, q, topic, page, pages, hint="Antwort auf der nächsten Folie  →"):
    img = background(brand)
    header(img, brand, topic, page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])

    qtext = q.get("social_question") or q["question"]
    qf, qs = fit_font(d, qtext, "InterDisplay-Bold", CW, 62, 40)
    lines = wrap(d, qtext, qf, CW)
    lh = int(qs * 1.22)
    of = font("Inter-Medium", 34)
    boxes = []
    for opt in q["options"]:
        ol = wrap(d, opt, of, CW - 104)
        boxes.append((ol, max(84, len(ol) * 44 + 40)))
    block = len(lines) * lh + 44 + sum(b + 18 for _, b in boxes) - 18
    y = TOP + max(0, (BOT - TOP - block) // 2)

    for ln in lines:
        d.text((MX, y), ln, font=qf, fill=txt + (255,), anchor="la")
        y += lh

    y += 44
    for i, (ol, box_h) in enumerate(boxes):
        rrect(img, [MX, y, W - MX, y + box_h], 22, (255, 255, 255, 16), (255, 255, 255, 54), 2)
        d.text((MX + 36, y + box_h / 2), "ABCD"[i], font=font("InterDisplay-Bold", 34),
               fill=acc + (255,), anchor="lm")
        ty = y + box_h / 2 - (len(ol) - 1) * 22
        for ln in ol:
            d.text((MX + 92, ty), ln, font=of, fill=txt + (255,), anchor="lm")
            ty += 44
        y += box_h + 18

    footer(img, brand, hint)
    return img


def slide_answer(brand, q, topic, page, pages, explanation):
    img = background(brand)
    header(img, brand, topic, page, pages)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])

    correct = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
    _af, _as = fit_font(d, max((q["options"][c] for c in correct), key=len),
                        "InterDisplay-Bold", CW - 104, 50, 32)
    _eh = len(wrap(d, explanation, font("Inter-Regular", 34), CW)) * 48
    _bh = sum(max(96, len(wrap(d, q["options"][c], _af, CW - 104)) * int(_as * 1.2) + 48) + 16
              for c in correct)
    block = 58 + _bh + 40 + _eh
    y0 = TOP + max(0, (BOT - TOP - block) // 2)
    d.text((MX, y0), "Richtig ist", font=font("Inter-Medium", 34), fill=dim + (255,), anchor="la")
    y = y0 + 58
    af, asz = fit_font(d, max((q["options"][c] for c in correct), key=len),
                       "InterDisplay-Bold", CW - 104, 50, 32)
    for c in correct:
        ol = wrap(d, q["options"][c], af, CW - 104)
        box_h = max(96, len(ol) * int(asz * 1.2) + 48)
        rrect(img, [MX, y, W - MX, y + box_h], 22, acc + (46,), acc + (220,), 3)
        d.text((MX + 36, y + box_h / 2), "ABCD"[c], font=font("InterDisplay-Bold", 36),
               fill=acc + (255,), anchor="lm")
        ty = y + box_h / 2 - (len(ol) - 1) * asz * 0.6
        for ln in ol:
            d.text((MX + 92, ty), ln, font=af, fill=txt + (255,), anchor="lm")
            ty += asz * 1.2
        y += box_h + 16

    y += 40
    ef = font("Inter-Regular", 34)
    for ln in wrap(d, explanation, ef, CW):
        if y > H - 190:
            break
        d.text((MX, y), ln, font=ef, fill=dim + (255,), anchor="la")
        y += 48

    footer(img, brand, "Üben statt raten  →")
    return img


def slide_cta(brand, q_total, page, pages):
    img = background(brand)
    header(img, brand, None, page, pages)
    d = ImageDraw.Draw(img)
    txt, dim = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"])
    cy = 520
    d.ellipse([W // 2 - 96, cy - 96, W // 2 + 96, cy + 96],
              fill=hex2rgb(brand["secondary"]) + (255,))
    d.text((W // 2, cy + 2), brand["mark"], font=font("InterDisplay-Bold", 100),
           fill=(255, 255, 255, 255), anchor="mm")
    d.text((W // 2, cy + 190), f"{q_total} Prüfungsfragen", font=font("InterDisplay-Bold", 56),
           fill=txt + (255,), anchor="mm")
    for i, ln in enumerate(["mit Erklärung zu jeder Antwort,", "Originalprüfungen und Lernkarten"]):
        d.text((W // 2, cy + 266 + i * 50), ln, font=font("Inter-Medium", 36),
               fill=dim + (255,), anchor="mm")
    footer(img, brand, brand["url"], highlight=True)
    return img


def render(qfile, brandfile, outdir, explanation, topic, q_total):
    q = json.load(open(qfile, encoding="utf-8"))
    brand = json.load(open(brandfile, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    pages = 3
    slides = [
        slide_question(brand, q, topic, 1, pages),
        slide_answer(brand, q, topic, 2, pages, explanation),
        slide_cta(brand, q_total, 3, pages),
    ]
    paths = []
    for i, s in enumerate(slides, 1):
        p = os.path.join(outdir, f"{q['id'].lower()}-{i}.jpg")
        s.convert("RGB").save(p, "JPEG", quality=92, optimize=True)
        paths.append(p)
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("question"); ap.add_argument("brand"); ap.add_argument("outdir")
    ap.add_argument("--explanation", default=""); ap.add_argument("--topic", default="")
    ap.add_argument("--total", default="1.393")
    a = ap.parse_args()
    for p in render(a.question, a.brand, a.outdir, a.explanation, a.topic, a.total):
        print(p)
