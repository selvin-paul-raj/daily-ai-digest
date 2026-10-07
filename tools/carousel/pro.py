#!/usr/bin/env python3
"""JOE carousel renderer. Usage: python3 pro.py spec.json outdir
Renders 1080x1350 slides (PNG) + carousel.pdf from a JSON spec."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, M = 1080, 1350, 80
BG1, BG2 = (11, 18, 32), (17, 26, 46)          # #0B1220 -> #111A2E
WHITE, BODY, MUTED = (241, 245, 249), (203, 213, 225), (148, 163, 184)
TRACK = (39, 50, 70)
ACCENTS = {"blue": "#3B82F6", "teal": "#14B8A6", "violet": "#8B5CF6",
           "amber": "#F59E0B", "green": "#22C55E"}

def F(w, s): return ImageFont.truetype(os.path.join(HERE, "fonts", f"Poppins-{w}.ttf"), s)
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def fit(d, text, weight, size, width, max_lines, min_size=20):
    while size > min_size:
        f = F(weight, size); ls = wrap(d, text, f, width)
        if len(ls) <= max_lines and all(d.textlength(l, font=f) <= width for l in ls): return f, ls
        size -= 2
    f = F(weight, min_size); return f, wrap(d, text, f, width)

def background(accent):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3))
        for x in range(W): px[x, y] = c
    glow = Image.new("L", (W, H), 0); g = ImageDraw.Draw(glow)
    g.ellipse((W - 420, -380, W + 380, 420), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (30, 64, 120)), img, glow)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    for x in range(0, W, 60): gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 7))
    for y in range(0, H, 60): gd.line([(0, y), (W, y)], fill=(255, 255, 255, 7))
    img = Image.alpha_composite(img.convert("RGBA"), grid)
    return img

def circle(img_path, d, ring, ring_w):
    av = Image.open(img_path).convert("RGB").resize((d, d), Image.LANCZOS)
    mask = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(mask).ellipse((0, 0, d * 4, d * 4), fill=255)
    mask = mask.resize((d, d), Image.LANCZOS)
    out = Image.new("RGBA", (d + 2 * ring_w, d + 2 * ring_w), (0, 0, 0, 0))
    rm = Image.new("L", (out.width * 4, out.height * 4), 0); ImageDraw.Draw(rm).ellipse((0, 0, out.width * 4, out.height * 4), fill=255)
    out.paste(Image.new("RGBA", out.size, ring + (255,)), (0, 0), rm.resize(out.size, Image.LANCZOS))
    out.paste(av, (ring_w, ring_w), mask)
    return out

def rounded(im, r):
    mask = Image.new("L", (im.width * 3, im.height * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mask.width, mask.height), r * 3, fill=255)
    out = im.convert("RGBA"); out.putalpha(mask.resize(im.size, Image.LANCZOS)); return out

def header(img, d, a, A):
    av = circle(a["avatar"], 66, A, 4); img.alpha_composite(av, (M, 80))
    d.text((M + 92, 86), a["name"], font=F("SemiBold", 28), fill=WHITE)
    d.text((M + 92, 124), a["tagline"], font=F("Regular", 21), fill=MUTED)

def footer(d, i, n, A, swipe=True):
    if swipe:
        f = F("SemiBold", 21); tw = d.textlength("SWIPE", font=f)
        d.text((W - M - 46 - tw, 1240), "SWIPE", font=f, fill=MUTED)
        y = 1253; d.line([(W - M - 38, y), (W - M, y)], fill=MUTED, width=3)
        d.line([(W - M - 10, y - 9), (W - M, y)], fill=MUTED, width=3); d.line([(W - M - 10, y + 9), (W - M, y)], fill=MUTED, width=3)
    d.rounded_rectangle((M, 1280, W - M, 1286), 3, fill=TRACK)
    d.rounded_rectangle((M, 1280, M + int((W - 2 * M) * (i + 1) / n), 1286), 3, fill=A)

def draw_block(d, y, items):
    for kind, font, lines, color, gap in items:
        for ln in lines:
            d.text((M, y), ln, font=font, fill=color); y += int(font.size * 1.18)
        y += gap
    return y

def block_height(items):
    return sum(len(l) * int(f.size * (1.38 if k == "body" else 1.14)) + g for k, f, l, _, g in items)

def render(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    acc = spec.get("accent", "blue"); A = hexrgb(ACCENTS.get(acc, acc))
    a = spec["author"]; a["avatar"] = os.path.join(HERE, a["avatar"]) if not os.path.isabs(a["avatar"]) else a["avatar"]
    slides = spec["slides"]; n = len(slides); paths = []
    CW = W - 2 * M
    for i, s in enumerate(slides):
        img = background(A); d = ImageDraw.Draw(img); t = s["type"]
        if t == "hook":
            header(img, d, a, A)
            f = F("SemiBold", 22); lab = s["label"].upper(); tw = d.textlength(lab, font=f)
            d.rounded_rectangle((M, 220, M + tw + 40, 270), 25, fill=A); d.text((M + 20, 229), lab, font=f, fill=WHITE)
            tf, tl = fit(d, s["title"], "Bold", 106, CW - 30, 3)
            y = 330
            for ln in tl: d.text((M, y), ln, font=tf, fill=WHITE); y += int(tf.size * 1.08)
            y += 18; d.rectangle((M, y, M + 120, y + 8), fill=A); y += 44
            bf, bl = fit(d, s.get("body", ""), "Regular", 40, CW, 2)
            for ln in bl: d.text((M, y), ln, font=bf, fill=MUTED); y += int(bf.size * 1.3)
            if s.get("hero"):
                hp = s["hero"] if os.path.isabs(s["hero"]) else os.path.join(HERE, s["hero"])
                top = max(y + 26, 840); bot = 1200; hh = bot - top
                hero = Image.open(hp).convert("RGB"); r = max(CW / hero.width, hh / hero.height)
                hero = hero.resize((int(hero.width * r) + 1, int(hero.height * r) + 1), Image.LANCZOS)
                l = (hero.width - CW) // 2; tp = (hero.height - hh) // 2
                img.alpha_composite(rounded(hero.crop((l, tp, l + CW, tp + hh)), 24), (M, top))
            footer(d, i, n, A)
        elif t in ("text", "stat", "take"):
            header(img, d, a, A)
            items = [("label", F("Bold", 26), [s["label"].upper()], A, 24)]
            if t == "stat":
                sf, sl = fit(d, s["stat"], "Bold", 210, CW, 1, 90)
                items.append(("stat", sf, sl, A, -6))
            tf, tl = fit(d, s["title"], "Bold", 74 if t != "stat" else 60, CW - 40, 2 if t != "stat" else 1, 36)
            items.append(("title", tf, tl, WHITE, 14))
            bf, bl = fit(d, s.get("body", ""), "Regular", 40, CW - (34 if t == "take" else 0), 5, 26)
            items.append(("body", bf, bl, BODY, 0))
            hgt = block_height(items); y0 = max(330, int((H - hgt) / 2) - 5)
            y = y0
            for kind, f, ls, col, gap in items:
                x = M + (34 if (t == "take" and kind == "body") else 0)
                if t == "take" and kind == "body":
                    d.rectangle((M, y + 6, M + 7, y + len(ls) * int(f.size * 1.38) - 10), fill=A)
                if kind == "stat": y -= int(f.size * 0.12)
                lh = 1.38 if kind == "body" else 1.14
                for ln in ls: d.text((x, y), ln, font=f, fill=col); y += int(f.size * lh)
                y += gap
            footer(d, i, n, A)
        elif t == "follow":
            av = circle(a["avatar"], 300, A, 6); img.alpha_composite(av, ((W - av.width) // 2, 118))
            def ctext(y, txt, f, col): d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col)
            ctext(468, a["name"], F("Bold", 44), WHITE); ctext(532, a["tagline"], F("Regular", 28), MUTED)
            tf, tl = fit(d, s.get("title", "Follow for daily AI news for builders"), "Bold", 64, CW - 40, 2)
            y = 610
            for ln in tl: ctext(y, ln, tf, WHITE); y += int(tf.size * 1.12)
            y += 26; bt = s.get("button", "FOLLOW"); bf = F("Bold", 31); bw = d.textlength(bt, font=bf) + 120
            d.rounded_rectangle(((W - bw) / 2, y, (W + bw) / 2, y + 80), 40, fill=A)
            ctext(y + 19, bt, bf, WHITE); y += 134
            hf = F("Regular", 34); icf = F("Bold", 22)
            widest = max(d.textlength(h["text"], font=hf) for h in a["handles"]) + 80
            x0 = int((W - widest) / 2)
            for h in a["handles"]:
                d.rounded_rectangle((x0, y, x0 + 56, y + 56), 10, fill=A)
                d.text((x0 + 28 - d.textlength(h["icon"], font=icf) / 2, y + 13), h["icon"], font=icf, fill=WHITE)
                d.text((x0 + 76, y + 6), h["text"], font=hf, fill=WHITE); y += 78
            ctext(max(y + 40, 1180), s.get("footer", "Save this · Share it with a builder"), F("Regular", 26), MUTED)
            footer(d, i, n, A, swipe=False)
        p = os.path.join(outdir, f"slide_{i+1:02d}.png"); img.convert("RGB").save(p); paths.append(p)
    ims = [Image.open(p).convert("RGB") for p in paths]
    pdf = os.path.join(outdir, "carousel.pdf")
    ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=150)
    return paths, pdf

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = sys.argv[2] if len(sys.argv) > 2 else "out"
    paths, pdf = render(spec, out); print("\n".join(paths)); print(pdf)
