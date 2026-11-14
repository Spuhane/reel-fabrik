#!/usr/bin/env python3
"""Quiz-Reel: Frage, Denkpause, Aufloesung. 1080x1920 MP4."""
import json, math, os, subprocess, argparse
from PIL import Image, ImageDraw
from render import (font, hex2rgb, wrap, fit_font, ease_out_cubic, clamp01, seg,
                    build_background, grain_tiles, W, H, FPS)

MX = 96
CW = W - 2 * MX
SAFE_TOP, SAFE_BOT = 300, 1430

T_Q, T_PAUSE, T_REVEAL, T_CTA = 0.3, 5.0, 8.2, 14.2
TOTAL = 17.4


def layer_rrect(img, box, radius, fill=None, outline=None, width=2):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, radius=radius, fill=fill,
                                          outline=outline, width=width)
    img.alpha_composite(lay)


def chip(img, brand, text, y):
    d = ImageDraw.Draw(img)
    f = font("Inter-SemiBold", 28)
    tw = d.textlength(text, font=f)
    acc = hex2rgb(brand["accent"])
    layer_rrect(img, [MX, y, MX + tw + 52, y + 62], 31, acc + (36,), acc + (130,), 2)
    d.text((MX + 26, y + 32), text, font=f, fill=acc + (255,), anchor="lm")


def brandline(img, brand):
    d = ImageDraw.Draw(img)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([MX, 300, MX + 60, 360], fill=hex2rgb(brand["secondary"]) + (255,))
    img.alpha_composite(lay)
    d.text((MX + 30, 330), brand["mark"], font=font("InterDisplay-Bold", 34),
           fill=(255, 255, 255, 255), anchor="mm")
    d.text((MX + 78, 330), brand["name"], font=font("InterDisplay-SemiBold", 32),
           fill=hex2rgb(brand["text"]) + (255,), anchor="lm")


def layout(d, q):
    qt = q.get("social_question") or q["question"]
    qf, qs = fit_font(d, qt, "InterDisplay-Bold", CW, 72, 46)
    qlines = wrap(d, qt, qf, CW)
    of = font("Inter-Medium", 40)
    boxes = [(wrap(d, o, of, CW - 112), ) for o in q["options"]]
    heights = [max(100, len(b[0]) * 50 + 48) for b in boxes]
    return qt, qf, qs, qlines, of, [b[0] for b in boxes], heights


def frame(brand, q, explanation, topic, t, bgfn):
    img = bgfn(t)
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    correct = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]

    brandline(img, brand)
    chip(img, brand, topic, 396)

    qt, qf, qs, qlines, of, olines, heights = layout(d, q)
    y = 468
    for i, ln in enumerate(qlines):
        p = ease_out_cubic(seg(t, T_Q + i * 0.1, 0.45))
        if p <= 0: continue
        d.text((MX, y + int((1 - p) * 34)), ln, font=qf, fill=txt + (int(255 * p),), anchor="la")
        y += int(qs * 1.2)

    y += 40
    revealing = t >= T_REVEAL
    rp = ease_out_cubic(seg(t, T_REVEAL, 0.5))
    for i, (ol, bh) in enumerate(zip(olines, heights)):
        p = ease_out_cubic(seg(t, T_Q + 0.5 + i * 0.16, 0.45))
        if p <= 0: break
        is_right = i in correct
        if revealing and is_right:
            fill = acc + (int((40 + 20 * rp) * p),)
            line = acc + (int(230 * p),)
            tcol = txt
            wdt = 3
        elif revealing:
            fill = (255, 255, 255, int(8 * p))
            line = (255, 255, 255, int(22 * p))
            tcol = tuple(int(c * (1 - 0.45 * rp)) for c in dim)
            wdt = 2
        else:
            fill = (255, 255, 255, int(16 * p))
            line = (255, 255, 255, int(52 * p))
            tcol = txt
            wdt = 2
        off = int((1 - p) * 30)
        layer_rrect(img, [MX, y + off, W - MX, y + off + bh], 24, fill, line, wdt)
        d.text((MX + 40, y + off + bh / 2), "ABCD"[i], font=font("InterDisplay-Bold", 40),
               fill=acc + (int(255 * p),), anchor="lm")
        ty = y + off + bh / 2 - (len(ol) - 1) * 25
        for ln in ol:
            d.text((MX + 108, ty), ln, font=of, fill=tcol + (int(255 * p),), anchor="lm")
            ty += 50
        y += bh + 20

    # Denkpause: Ring mit Countdown
    if T_PAUSE <= t < T_REVEAL:
        left = T_REVEAL - t
        frac = clamp01(left / (T_REVEAL - T_PAUSE))
        cx, cy, r = W // 2, y + 110, 62
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 40), width=8)
        ld.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + int(360 * frac),
               fill=acc + (255,), width=8)
        img.alpha_composite(lay)
        d.text((cx, cy + 2), str(max(1, math.ceil(left))), font=font("InterDisplay-Bold", 54),
               fill=txt + (255,), anchor="mm")
    elif t < T_PAUSE and t > T_Q + 1.4:
        p = ease_out_cubic(seg(t, T_Q + 1.4, 0.5))
        d.text((W // 2, y + 70), "Welche ist richtig?", font=font("Inter-Medium", 38),
               fill=dim + (int(255 * p),), anchor="mm")

    # Erklaerung nach der Aufloesung
    if t >= T_REVEAL + 0.6:
        p = ease_out_cubic(seg(t, T_REVEAL + 0.6, 0.5))
        ef = font("Inter-Regular", 34)
        ey = y + 44
        for ln in wrap(d, explanation, ef, CW):
            if ey > SAFE_BOT - 50: break
            d.text((MX, ey + int((1 - p) * 18)), ln, font=ef, fill=dim + (int(255 * p),), anchor="la")
            ey += 46

    # CTA-Pille
    if t >= T_CTA:
        p = ease_out_cubic(seg(t, T_CTA, 0.5))
        f = font("Inter-SemiBold", 38)
        tw = d.textlength(brand["url"], font=f)
        pw, ph = int(tw) + 86, 90
        layer_rrect(img, [(W - pw) // 2, SAFE_BOT - ph, (W + pw) // 2, SAFE_BOT], 45,
                    acc + (int(245 * p),))
        d.text((W / 2, SAFE_BOT - ph / 2), brand["url"], font=f,
               fill=(10, 10, 12, int(255 * p)), anchor="mm")

    # Fortschrittsbalken
    layer_rrect(img, [MX, 272, W - MX, 278], 3, (255, 255, 255, 36))
    x2 = MX + (W - 2 * MX) * clamp01(t / TOTAL)
    if x2 > MX + 6:
        layer_rrect(img, [MX, 272, x2, 278], 3, acc + (230,))
    return img


def render(post, brandfile, out):
    p = json.load(open(post, encoding="utf-8"))
    brand = json.load(open(brandfile, encoding="utf-8"))
    q, expl, topic = p["question"], p["explanation"], p["topic"]
    bg_big, pad = build_background(brand)
    grains = grain_tiles()

    def bgfn(t):
        dx = pad + int(math.sin(t * 0.17) * pad * 0.5)
        dy = pad + int(math.cos(t * 0.13) * pad * 0.5)
        return bg_big.crop((dx, dy, dx + W, dy + H)).convert("RGBA")

    work = "work/qframes"
    os.makedirs(work, exist_ok=True)
    subprocess.run(f"rm -f {work}/*.png", shell=True)
    n = int(TOTAL * FPS)
    for f in range(n):
        im = frame(brand, q, expl, topic, f / FPS, bgfn).convert("RGB")
        g = grains[f % len(grains)]
        im = Image.blend(im, Image.blend(im, g, 0.5), 0.08)
        im.save(f"{work}/{f:05d}.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", f"{work}/%05d.png", "-f", "lavfi", "-t", f"{TOTAL:.2f}",
                    "-i", "anullsrc=r=44100:cl=stereo",
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run(f"rm -f {work}/*.png", shell=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post"); ap.add_argument("brand"); ap.add_argument("out")
    a = ap.parse_args()
    print(render(a.post, a.brand, a.out))
