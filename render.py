#!/usr/bin/env python3
"""Reel-Renderer: Tipp-JSON + Brand-Config -> 1080x1920 MP4 (Instagram Reel)."""
import json, math, os, subprocess, sys, argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/opentype/inter"

# Instagram-Reels-Safe-Zone
SAFE_TOP, SAFE_BOTTOM = 300, 1440
MARGIN_X = 96
CONTENT_W = W - 2 * MARGIN_X


def font(style, size):
    return ImageFont.truetype(f"{FONT_DIR}/{style}.otf", size)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------- Easing ----------
def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    return 3 * t * t - 2 * t * t * t


def clamp01(x):
    return max(0.0, min(1.0, x))


def seg(t, start, dur):
    """Fortschritt 0..1 eines Zeitabschnitts."""
    if dur <= 0:
        return 1.0
    return clamp01((t - start) / dur)


# ---------- Text ----------
def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words, cur = para.split(), ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def fit_font(draw, text, style, max_w, start, min_size=52, step=3):
    """Verkleinert die Schrift, bis jede manuelle Zeile in max_w passt."""
    size = start
    while size > min_size:
        fnt = font(style, size)
        if all(draw.textlength(ln, font=fnt) <= max_w for ln in text.split("\n") if ln.strip()):
            return fnt, size
        size -= step
    return font(style, min_size), min_size


def draw_lines(draw, lines, fnt, x, y, line_h, fill, anchor="la"):
    for i, ln in enumerate(lines):
        draw.text((x, y + i * line_h), ln, font=fnt, fill=fill, anchor=anchor)
    return y + len(lines) * line_h


# ---------- Hintergrund ----------
def build_background(brand, pad=260):
    """Grosse Glow-Leinwand; pro Frame wird ein wanderndes Fenster ausgeschnitten."""
    bw, bh = W + 2 * pad, H + 2 * pad
    base = Image.new("RGB", (bw, bh), hex2rgb(brand["bg"]))

    def radial(cx, cy, radius, color, strength):
        yy, xx = np.mgrid[0:bh, 0:bw]
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / radius
        a = np.clip(1.0 - d, 0, 1) ** 2.2 * strength
        layer = np.zeros((bh, bw, 3), dtype=np.float32)
        for i, c in enumerate(color):
            layer[:, :, i] = c
        return layer, a[:, :, None]

    arr = np.asarray(base, dtype=np.float32)
    for cx, cy, r, col, s in [
        (bw * 0.78, bh * 0.20, bw * 0.62, hex2rgb(brand["accent"]), 0.30),
        (bw * 0.16, bh * 0.74, bw * 0.58, hex2rgb(brand["secondary"]), 0.20),
        (bw * 0.50, bh * 0.50, bw * 0.75, hex2rgb(brand["accent_soft"]), 0.055),
    ]:
        layer, a = radial(cx, cy, r, col, s)
        arr = arr * (1 - a) + layer * a

    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img.filter(ImageFilter.GaussianBlur(70)), pad


def grain_tiles(n=6, strength=7):
    rng = np.random.default_rng(7)
    out = []
    for _ in range(n):
        noise = rng.normal(0, strength, (H // 2, W // 2, 1)).repeat(3, axis=2)
        tile = Image.fromarray(np.clip(noise + 128, 0, 255).astype(np.uint8))
        out.append(tile.resize((W, H), Image.BILINEAR))
    return out


# ---------- Bausteine ----------
def draw_badge(img, brand, alpha=1.0):
    """Schräges Marken-Badge oben (Logo-Mark + Name)."""
    if alpha <= 0.01:
        return
    bw, bh = 640, 112
    badge = Image.new("RGBA", (bw + 60, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    ox, oy = 30, 30
    acc, txt, dim = hex2rgb(brand["accent"]), hex2rgb(brand["text"]), hex2rgb(brand["text_dim"])

    d.rounded_rectangle([ox, oy, ox + bw, oy + bh], radius=56, fill=(255, 255, 255, 12),
                        outline=acc + (120,), width=2)
    d.ellipse([ox + 16, oy + 16, ox + 16 + 80, oy + 16 + 80], fill=hex2rgb(brand["secondary"]) + (255,))
    mark_f = font("InterDisplay-Bold", 44 if len(brand["mark"]) == 1 else 34)
    d.text((ox + 56, oy + 56), brand["mark"], font=mark_f, fill=(255, 255, 255, 255), anchor="mm")
    d.text((ox + 116, oy + 36), brand["name"], font=font("InterDisplay-SemiBold", 36),
           fill=txt + (255,), anchor="lm")
    d.text((ox + 116, oy + 76), brand["badge_text"], font=font("Inter-Medium", 23),
           fill=dim + (255,), anchor="lm")

    # Badge gerade - schraeg wurde verworfen (Stefan, 14.11.2026)
    if alpha < 1.0:
        a = badge.getchannel("A").point(lambda v: int(v * alpha))
        badge.putalpha(a)
    img.alpha_composite(badge, (MARGIN_X - 30, 332))


def draw_url_pill(img, brand, alpha=1.0):
    if alpha <= 0.01:
        return
    fnt = font("Inter-SemiBold", 34)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = tmp.textlength(brand["url"], font=fnt)
    pw, ph = int(tw) + 88, 82
    pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    acc = hex2rgb(brand["accent"])
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=41, fill=acc + (235,))
    d.text((pw / 2, ph / 2 + 1), brand["url"], font=fnt, fill=(10, 10, 12, 255), anchor="mm")
    if alpha < 1.0:
        pill.putalpha(pill.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(pill, ((W - pw) // 2, 1332))


def draw_progress(img, brand, p):
    d = ImageDraw.Draw(img)
    acc = hex2rgb(brand["accent"])
    y = 258
    d.rounded_rectangle([MARGIN_X, y, W - MARGIN_X, y + 6], radius=3, fill=(255, 255, 255, 36))
    x2 = MARGIN_X + (W - 2 * MARGIN_X) * clamp01(p)
    if x2 > MARGIN_X + 6:
        d.rounded_rectangle([MARGIN_X, y, x2, y + 6], radius=3, fill=acc + (230,))


def draw_underline(img, brand, x, y, width, p, thickness=14):
    """Handgezeichnet wirkender Akzent-Strich, der einwischt."""
    if p <= 0:
        return
    w = int(width * ease_out_cubic(p))
    if w < 4:
        return
    strip = Image.new("RGBA", (max(w, 1), thickness * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(strip)
    acc = hex2rgb(brand["accent"])
    pts = []
    for i in range(0, w, 8):
        t = i / max(width, 1)
        pts.append((i, thickness * 1.5 + math.sin(t * 5.2) * 4.0))
    if len(pts) > 1:
        d.line(pts, fill=acc + (255,), width=thickness, joint="curve")
    img.alpha_composite(strip, (int(x), int(y)))


# ---------- Szenen ----------
def scene_hook(img, brand, data, t, t0, dur):
    d = ImageDraw.Draw(img)
    txt = hex2rgb(brand["text"])
    fnt, fsize = fit_font(d, data["hook"], "InterDisplay-Bold", CONTENT_W, 88, 58)
    lines = [ln for ln in data["hook"].split("\n") if ln.strip()]
    line_h = int(fsize * 1.24)
    y = SAFE_TOP + 200

    for i, ln in enumerate(lines):
        p = ease_out_cubic(seg(t, t0 + i * 0.13, 0.55))
        if p <= 0:
            continue
        off = int((1 - p) * 46)
        d.text((MARGIN_X, y + i * line_h + off), ln, font=fnt,
               fill=txt + (int(255 * p),), anchor="la")

    last_w = d.textlength(lines[-1], font=fnt) if lines else 0
    up = seg(t, t0 + len(lines) * 0.13 + 0.25, 0.5)
    draw_underline(img, brand, MARGIN_X, y + len(lines) * line_h - 18, last_w * 0.92, up)

    sub = data.get("hook_sub")
    if sub:
        p = ease_out_cubic(seg(t, t0 + 0.85, 0.5))
        if p > 0:
            sf = font("Inter-Medium", 38)
            sl = wrap(d, sub, sf, CONTENT_W)
            sy = y + len(lines) * line_h + 58
            for i, ln in enumerate(sl):
                d.text((MARGIN_X, sy + i * 50 + int((1 - p) * 24)), ln, font=sf,
                       fill=hex2rgb(brand["text_dim"]) + (int(255 * p),), anchor="la")


def scene_points(img, brand, data, t, t0, step):
    d = ImageDraw.Draw(img)
    acc, txt, dim = hex2rgb(brand["accent"]), hex2rgb(brand["text"]), hex2rgb(brand["text_dim"])
    y = SAFE_TOP + 232
    fnt = font("InterDisplay-SemiBold", 54)
    sub_f = font("Inter-Regular", 34)
    body_lh, gap = 44, 48

    for i, pt in enumerate(data["points"]):
        start = t0 + i * step
        p = ease_out_cubic(seg(t, start, 0.55))
        if p <= 0:
            break
        a = int(255 * p)
        off = int((1 - p) * 40)
        title = pt["title"] if isinstance(pt, dict) else pt
        body = pt.get("body") if isinstance(pt, dict) else None

        # Index-Marker
        mx, my = MARGIN_X, y + off
        marker = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(marker).rounded_rectangle(
            [mx, my, mx + 62, my + 62], radius=20,
            fill=acc + (int(38 * p),), outline=acc + (int(170 * p),), width=2)
        img.alpha_composite(marker)
        d.text((mx + 31, my + 33), str(i + 1), font=font("InterDisplay-Bold", 34),
               fill=acc + (a,), anchor="mm")

        tx = MARGIN_X + 92
        tlines = wrap(d, title, fnt, CONTENT_W - 92)
        for j, ln in enumerate(tlines):
            d.text((tx, y + off + j * 64 - 2), ln, font=fnt, fill=txt + (a,), anchor="la")
        yy = y + len(tlines) * 64 + 6

        if body:
            blines = wrap(d, body, sub_f, CONTENT_W - 92)
            for j, ln in enumerate(blines):
                d.text((tx, yy + off + j * body_lh), ln, font=sub_f, fill=dim + (a,), anchor="la")
            yy += len(blines) * body_lh
        y = yy + gap


def scene_outro(img, brand, data, t, t0):
    d = ImageDraw.Draw(img)
    txt, dim, acc = hex2rgb(brand["text"]), hex2rgb(brand["text_dim"]), hex2rgb(brand["accent"])
    p = ease_out_cubic(seg(t, t0, 0.6))
    if p <= 0:
        return
    a = int(255 * p)
    cy = SAFE_TOP + 420

    r = 92
    scale = 0.86 + 0.14 * p
    rr = int(r * scale)
    d.ellipse([W // 2 - rr, cy - rr, W // 2 + rr, cy + rr],
              fill=hex2rgb(brand["secondary"]) + (a,))
    d.text((W // 2, cy + 2), brand["mark"],
           font=font("InterDisplay-Bold", int(96 if len(brand["mark"]) == 1 else 68)),
           fill=(255, 255, 255, a), anchor="mm")

    d.text((W // 2, cy + 190), brand["name"], font=font("InterDisplay-Bold", 62),
           fill=txt + (a,), anchor="mm")

    p2 = ease_out_cubic(seg(t, t0 + 0.35, 0.55))
    if p2 > 0:
        a2 = int(255 * p2)
        cta = data.get("outro", "Jetzt kostenlos testen")
        cf = font("Inter-Medium", 40)
        cl = wrap(d, cta, cf, CONTENT_W - 60)
        for i, ln in enumerate(cl):
            d.text((W // 2, cy + 280 + i * 54 + int((1 - p2) * 20)), ln, font=cf,
                   fill=dim + (a2,), anchor="mm")


# ---------- Hauptschleife ----------
def render(tip_path, brand_path, out_path, keep_frames=False):
    data = json.load(open(tip_path, encoding="utf-8"))
    brand = json.load(open(brand_path, encoding="utf-8"))

    n_points = len(data["points"])
    hook_dur = data.get("hook_dur", 3.2)
    step = data.get("point_step", 1.9)
    points_dur = step * n_points + 1.3
    outro_dur = data.get("outro_dur", 3.2)
    total = hook_dur + points_dur + outro_dur
    n_frames = int(total * FPS)

    bg_big, pad = build_background(brand)
    grains = grain_tiles()
    work = "work/frames"
    os.makedirs(work, exist_ok=True)
    subprocess.run(f"rm -f {work}/*.png", shell=True)

    t_points = hook_dur
    t_outro = hook_dur + points_dur

    for f in range(n_frames):
        t = f / FPS
        # wanderndes Hintergrundfenster
        dx = pad + int(math.sin(t * 0.17) * pad * 0.55)
        dy = pad + int(math.cos(t * 0.13) * pad * 0.55)
        frame = bg_big.crop((dx, dy, dx + W, dy + H)).convert("RGBA")

        draw_progress(frame, brand, t / total)

        if t < t_points:
            draw_badge(frame, brand, 1.0)
            fade = 1.0 - clamp01((t - (t_points - 0.35)) / 0.35)
            scene_hook(frame, brand, data, t, 0.25, hook_dur)
            if fade < 1.0:
                frame = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), frame, fade) \
                    if False else frame
        elif t < t_outro:
            draw_badge(frame, brand, 1.0)
            scene_points(frame, brand, data, t, t_points + 0.1, step)
            draw_url_pill(frame, brand, clamp01((t - t_points - 0.5) / 0.5))
        else:
            scene_outro(frame, brand, data, t, t_outro + 0.1)
            draw_url_pill(frame, brand, clamp01((t - t_outro - 0.4) / 0.5))

        out = frame.convert("RGB")
        g = grains[f % len(grains)]
        out = Image.blend(out, Image.blend(out, g, 0.5), 0.085)
        out.save(f"{work}/{f:05d}.png")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS), "-i", f"{work}/%05d.png",
        "-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "slow",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart", out_path,
    ]
    subprocess.run(cmd, check=True)
    if not keep_frames:
        subprocess.run(f"rm -f {work}/*.png", shell=True)
    return out_path, total, n_frames


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tip")
    ap.add_argument("brand")
    ap.add_argument("out")
    ap.add_argument("--keep-frames", action="store_true")
    a = ap.parse_args()
    p, total, nf = render(a.tip, a.brand, a.out, a.keep_frames)
    print(f"{p}  {total:.1f}s  {nf} frames")
