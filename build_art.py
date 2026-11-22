#!/usr/bin/env python3
"""Generate every product image as SVG.

One drawing language across four lines: soft studio light, generous radii, a single
crisp shadow and a hint of material. Colours are derived from the product's own hex so
a new finish only needs one value.

Output: assets/products/<id>.svg  (one per product, plus a hero and journal ornaments)

Run: python3 build_art.py
"""
import colorsys
import pathlib
import re

OUT = pathlib.Path(__file__).resolve().parent / "assets" / "products"

# id, form, base colour, secondary accent
ART = [
    ("spring-01", "fountain", "#c3cace", None),
    ("spring-02", "fountain-ceramic", "#efe7da", None),
    ("spring-mini", "fountain", "#dfe4e6", "small"),
    ("feast-01", "feeder", "#efe9dd", None),
    ("feast-mini", "feeder", "#e4d6bf", "small"),
    ("still-bowl", "bowl", "#eee7db", None),
    ("still-mat", "mat", "#dccbb0", None),
    ("play-snuffle", "snuffle", "#e6d9c2", None),
    ("play-ball", "ball", "#e8734a", None),
    ("filter-3", "filter", "#e9e6df", None),
    ("pump", "pump", "#cfd5d8", None),
]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    clamp = lambda v: max(0, min(255, int(round(v * 255))))
    return "#%02x%02x%02x" % (clamp(r), clamp(g), clamp(b))


def tone(base, dl=0.0, ds=0.0, dh=0.0):
    """Lightness / saturation / hue shift of a base hex."""
    r, g, b = hex_to_rgb(base)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + dh) % 1.0
    l = max(0.03, min(0.98, l + dl))
    s = max(0.0, min(1.0, s + ds))
    return rgb_to_hex(*colorsys.hls_to_rgb(h, l, s))


def pal(base):
    return {
        "hi": tone(base, 0.24, -0.04),
        "light": tone(base, 0.12, -0.02),
        "mid": base,
        "low": tone(base, -0.12, 0.02),
        "dark": tone(base, -0.28, 0.04),
        "deep": tone(base, -0.42, 0.05),
        "line": tone(base, -0.34, 0.06),
    }


SHADOW = ('<ellipse cx="310" cy="{y}" rx="{rx}" ry="{ry}" fill="#14201f" opacity=".16" '
          'filter="url(#soft)"/>')
DEFS = """<defs>
  <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{hi}"/>
    <stop offset=".22" stop-color="{light}"/>
    <stop offset=".55" stop-color="{mid}"/>
    <stop offset=".82" stop-color="{low}"/>
    <stop offset="1" stop-color="{dark}"/>
  </linearGradient>
  <linearGradient id="v" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{dark}" stop-opacity=".55"/>
    <stop offset=".22" stop-color="{hi}" stop-opacity=".55"/>
    <stop offset=".55" stop-color="{hi}" stop-opacity=".05"/>
    <stop offset="1" stop-color="{dark}" stop-opacity=".5"/>
  </linearGradient>
  <linearGradient id="w" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#dff2f6"/>
    <stop offset="1" stop-color="#a9d3e0"/>
  </linearGradient>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="s2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>"""


def svg(inner, label, base):
    p = pal(base)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 760" width="620" height="760" '
            f'role="img" aria-label="{label}">{DEFS.format(**p)}'
            f'<ellipse cx="310" cy="330" rx="250" ry="260" fill="url(#w)" opacity=".10"/>'
            f'{inner}</svg>')


def fountain(p, small=False):
    t = pal(p)
    w = 0.86 if small else 1.0
    x0, x1 = 310 - 212 * w, 310 + 212 * w
    top, bot = 300, 690 if not small else 660
    return svg(f"""
{SHADOW.format(y=bot + 22, rx=190 * w, ry=26)}
<path d="M{x0} 360 C{x0} 330 {310 - 118 * w} 302 {310} 302 C{310 + 118 * w} 302 {x1} 330 {x1} 360
         L{x1 - 18 * w} {bot - 44} C{x1 - 22 * w} {bot - 8} {310 + 96 * w} {bot} {310} {bot}
         C{310 - 96 * w} {bot} {x0 + 22 * w} {bot - 8} {x0 + 18 * w} {bot - 44} Z"
      fill="url(#g)"/>
<path d="M{x0} 360 C{x0} 330 {310 - 118 * w} 302 {310} 302 C{310 + 118 * w} 302 {x1} 330 {x1} 360
         L{x1 - 18 * w} {bot - 44} C{x1 - 22 * w} {bot - 8} {310 + 96 * w} {bot} {310} {bot}
         C{310 - 96 * w} {bot} {x0 + 22 * w} {bot - 8} {x0 + 18 * w} {bot - 44} Z"
      fill="url(#v)" opacity=".85"/>
<ellipse cx="310" cy="352" rx="{212 * w}" ry="56" fill="{t['hi']}"/>
<ellipse cx="310" cy="346" rx="{212 * w}" ry="56" fill="url(#g)"/>
<ellipse cx="310" cy="344" rx="{190 * w}" ry="49" fill="{t['dark']}"/>
<ellipse cx="310" cy="347" rx="{188 * w}" ry="47" fill="url(#w)" opacity=".92"/>
<ellipse cx="310" cy="341" rx="30" ry="9" fill="#14201f" opacity=".16"/>
<path d="M286 342 C288 323 332 323 334 342 Z" fill="{t['hi']}" opacity=".38"/>
<path d="M291 342 C293 327 327 327 329 342 Z" fill="#eaf7fa" opacity=".65"/>
<g fill="none" stroke="#eaf7fa" stroke-width="1.4" opacity=".7">
  <ellipse cx="310" cy="348" rx="34" ry="10"/>
  <ellipse cx="310" cy="352" rx="66" ry="18" opacity=".45"/>
</g>
<rect x="{310 + 96 * w}" y="410" width="13" height="170" rx="6.5" fill="{t['deep']}" opacity=".45"/>
<rect x="{310 + 98 * w}" y="412" width="9" height="166" rx="4.5" fill="#0f2a2a" opacity=".28"/>
<rect x="{310 + 98 * w}" y="492" width="9" height="86" rx="4.5" fill="#8fc3d4" opacity=".75"/>
<path d="M{x0} 360 C{x0} 330 {310 - 118 * w} 302 {310} 302 C{310 + 118 * w} 302 {x1} 330 {x1} 360
         L{x1 - 18 * w} {bot - 44} C{x1 - 22 * w} {bot - 8} {310 + 96 * w} {bot} {310} {bot}
         C{310 - 96 * w} {bot} {x0 + 22 * w} {bot - 8} {x0 + 18 * w} {bot - 44} Z"
      fill="none" stroke="{t['hi']}" stroke-width="1.4" opacity=".55"/>
<path d="M{x0 + 26} 386 C{x0 + 26} 372 {x0 + 40} 366 {x0 + 54} 364 L{x0 + 62} {bot - 60} C{x0 + 46} {bot - 64} {x0 + 32} {bot - 72} {x0 + 30} {bot - 86} Z" fill="#fff" opacity=".35" filter="url(#s2)"/>
""", "Asiajoly fountain", p)


def fountain_ceramic(p):
    t = pal(p)
    return svg(f"""
{SHADOW.format(y=700, rx=186, ry=24)}
<path d="M104 372 C104 340 200 312 310 312 C420 312 516 340 516 372
         L500 636 C498 672 414 692 310 692 C206 692 122 672 120 636 Z" fill="url(#g)"/>
<path d="M104 372 C104 340 200 312 310 312 C420 312 516 340 516 372
         L500 636 C498 672 414 692 310 692 C206 692 122 672 120 636 Z" fill="url(#v)" opacity=".7"/>
<ellipse cx="310" cy="364" rx="212" ry="56" fill="{t['hi']}"/>
<ellipse cx="310" cy="358" rx="212" ry="56" fill="url(#g)"/>
<ellipse cx="310" cy="358" rx="188" ry="48" fill="{t['dark']}" opacity=".9"/>
<ellipse cx="310" cy="361" rx="186" ry="46" fill="url(#w)" opacity=".9"/>
<ellipse cx="310" cy="356" rx="26" ry="8" fill="#14201f" opacity=".14"/>
<path d="M288 357 C290 340 330 340 332 357 Z" fill="#fbf7ee" opacity=".7"/>
<path d="M118 402 C120 470 138 560 168 610" stroke="#fff" stroke-width="3" fill="none" opacity=".3" filter="url(#s2)"/>
<path d="M110 380 C150 350 240 332 310 332" stroke="#fff" stroke-width="2" fill="none" opacity=".22"/>
""", "Asiajoly ceramic fountain", p)


def feeder(p, small=False, camera=False):
    t = pal(p)
    s = 0.86 if small else 1.0
    w = 330 * s
    h = 380 * s
    x = 310 - w / 2
    y = 690 - h
    cam = f"""
<rect x="{310 - 46}" y="{y + 54}" width="92" height="62" rx="14" fill="#1b2b2b"/>
<circle cx="310" cy="{y + 85}" r="20" fill="#0d1a1a"/>
<circle cx="310" cy="{y + 85}" r="11" fill="#2a5b6b"/>
<circle cx="{310 + 5}" cy="{y + 80}" r="3.5" fill="#cfeef7" opacity=".9"/>""" if camera else ""
    return svg(f"""
{SHADOW.format(y=706, rx=150 * s, ry=22)}
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{34 * s}" fill="url(#g)"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{34 * s}" fill="url(#v)" opacity=".55"/>
<rect x="{x + 8}" y="{y - 14}" width="{w - 16}" height="{30}" rx="15" fill="{t['light']}"/>
<rect x="{x + 8}" y="{y - 10}" width="{w - 16}" height="{18}" rx="9" fill="{t['mid']}" opacity=".55"/>
<rect x="{x + 26}" y="{y + 128}" width="{w - 52}" height="{h - 190}" rx="{22 * s}" fill="{t['deep']}" opacity=".2"/>
<rect x="{310 - 74 * s}" y="{y + h - 150}" width="{148 * s}" height="{96 * s}" rx="{30 * s}" fill="{t['dark']}" opacity=".5"/>
<ellipse cx="310" cy="{y + h - 108 * s}" rx="{64 * s}" ry="{26 * s}" fill="{t['light']}"/>
<ellipse cx="310" cy="{y + h - 112 * s}" rx="{58 * s}" ry="{22 * s}" fill="{t['deep']}" opacity=".35"/>
{cam}
<rect x="{x + 30}" y="{y + 150}" width="{w - 60}" height="4" rx="2" fill="{t['deep']}" opacity=".18"/>
<circle cx="{310 + 96 * s}" cy="{y + 200}" r="7" fill="#12736b" opacity=".9"/>
<circle cx="{310 + 96 * s}" cy="{y + 200}" r="12" fill="#12736b" opacity=".18"/>
<path d="M{x + 24} {y + 30} C{x + 24} {y + 18} {x + 40} {y + 14} {x + 54} {y + 14} L{x + 60} {y + h - 40} C{x + 44} {y + h - 44} {x + 30} {y + h - 54} {x + 28} {y + h - 68} Z" fill="#fff" opacity=".32" filter="url(#s2)"/>
""", "Asiajoly feeder", p)


def bowl(p):
    t = pal(p)
    return svg(f"""
{SHADOW.format(y=608, rx=150, ry=20)}
<path d="M150 372 C150 344 220 322 310 322 C400 322 470 344 470 372
         L444 560 C440 588 380 600 310 600 C240 600 180 588 176 560 Z" fill="url(#g)"/>
<path d="M150 372 C150 344 220 322 310 322 C400 322 470 344 470 372
         L444 560 C440 588 380 600 310 600 C240 600 180 588 176 560 Z" fill="url(#v)" opacity=".6"/>
<ellipse cx="310" cy="366" rx="160" ry="44" fill="{t['hi']}"/>
<ellipse cx="310" cy="370" rx="146" ry="38" fill="{t['dark']}" opacity=".8"/>
<ellipse cx="310" cy="374" rx="144" ry="36" fill="url(#w)" opacity=".55"/>
<ellipse cx="310" cy="372" rx="120" ry="28" fill="none" stroke="#fff" stroke-width="1.4" opacity=".3"/>
<path d="M176 400 C182 500 214 560 254 578" stroke="#fff" stroke-width="2.6" fill="none" opacity=".25" filter="url(#s2)"/>
""", "Asiajoly bowl", p)


def mat(p):
    t = pal(p)
    return svg(f"""
<ellipse cx="310" cy="560" rx="200" ry="34" fill="#14201f" opacity=".12" filter="url(#soft)"/>
<rect x="96" y="380" width="428" height="170" rx="34" fill="{t['mid']}"/>
<rect x="96" y="380" width="428" height="170" rx="34" fill="url(#v)" opacity=".35"/>
<rect x="112" y="396" width="396" height="138" rx="26" fill="none" stroke="{t['hi']}" stroke-width="2" opacity=".7"/>
<rect x="128" y="410" width="364" height="110" rx="20" fill="{t['low']}" opacity=".35"/>
<g fill="{t['deep']}" opacity=".18">
  <circle cx="180" cy="466" r="4"/><circle cx="230" cy="466" r="4"/><circle cx="280" cy="466" r="4"/>
  <circle cx="330" cy="466" r="4"/><circle cx="380" cy="466" r="4"/><circle cx="430" cy="466" r="4"/>
</g>
""", "Asiajoly mat", p)


def snuffle(p):
    t = pal(p)
    return svg(f"""
<ellipse cx="310" cy="560" rx="196" ry="32" fill="#14201f" opacity=".14" filter="url(#soft)"/>
<rect x="112" y="356" width="396" height="196" rx="42" fill="{t['mid']}"/>
<rect x="112" y="356" width="396" height="196" rx="42" fill="url(#v)" opacity=".3"/>
<g stroke="{t['dark']}" stroke-width="7" stroke-linecap="round" opacity=".55" fill="none">
  <path d="M164 400 C196 448 160 486 196 516"/><path d="M220 396 C252 444 216 482 252 512"/>
  <path d="M276 400 C308 448 272 486 308 516"/><path d="M332 396 C364 444 328 482 364 512"/>
  <path d="M388 400 C420 448 384 486 420 516"/><path d="M444 404 C470 444 440 478 468 508"/>
</g>
<g stroke="{t['hi']}" stroke-width="3" stroke-linecap="round" opacity=".7" fill="none">
  <path d="M170 404 C202 452 166 490 202 520"/><path d="M282 404 C314 452 278 490 314 520"/>
  <path d="M394 404 C426 452 390 490 426 520"/>
</g>
""", "Asiajoly snuffle mat", p)


def ball(p):
    t = pal(p)
    return svg(f"""
{SHADOW.format(y=614, rx=126, ry=20)}
<circle cx="310" cy="470" r="142" fill="url(#g)"/>
<circle cx="310" cy="470" r="142" fill="url(#v)" opacity=".45"/>
<circle cx="310" cy="470" r="142" fill="none" stroke="{t['hi']}" stroke-width="2" opacity=".5"/>
<circle cx="310" cy="470" r="34" fill="{t['deep']}" opacity=".75"/>
<circle cx="310" cy="470" r="26" fill="#14201f" opacity=".55"/>
<circle cx="310" cy="470" r="18" fill="#2a1a12" opacity=".8"/>
<g fill="{t['hi']}" opacity=".55">
  <circle cx="250" cy="404" r="9"/><circle cx="360" cy="392" r="7"/><circle cx="392" cy="500" r="8"/>
  <circle cx="238" cy="520" r="7"/><circle cx="300" cy="360" r="6"/><circle cx="368" cy="556" r="6"/>
</g>
<ellipse cx="264" cy="404" rx="42" ry="26" fill="#fff" opacity=".28" transform="rotate(-24 264 404)" filter="url(#s2)"/>
""", "Asiajoly play ball", p)


def filter(p):
    t = pal(p)
    return svg(f"""
{SHADOW.format(y=596, rx=104, ry=18)}
<rect x="212" y="330" width="196" height="248" rx="28" fill="url(#g)"/>
<rect x="212" y="330" width="196" height="248" rx="28" fill="url(#v)" opacity=".5"/>
<ellipse cx="310" cy="340" rx="98" ry="26" fill="{t['hi']}"/>
<ellipse cx="310" cy="344" rx="86" ry="21" fill="{t['deep']}" opacity=".5"/>
<g fill="{t['deep']}" opacity=".3">
  <circle cx="270" cy="420" r="5"/><circle cx="310" cy="420" r="5"/><circle cx="350" cy="420" r="5"/>
  <circle cx="270" cy="462" r="5"/><circle cx="310" cy="462" r="5"/><circle cx="350" cy="462" r="5"/>
  <circle cx="270" cy="504" r="5"/><circle cx="310" cy="504" r="5"/><circle cx="350" cy="504" r="5"/>
</g>
<rect x="212" y="536" width="196" height="20" rx="10" fill="{t['deep']}" opacity=".35"/>
""", "Asiajoly filter", p)


def pump(p):
    t = pal(p)
    return svg(f"""
{SHADOW.format(y=566, rx=84, ry=16)}
<rect x="248" y="330" width="124" height="220" rx="26" fill="url(#g)"/>
<rect x="248" y="330" width="124" height="220" rx="26" fill="url(#v)" opacity=".45"/>
<ellipse cx="310" cy="340" rx="62" ry="17" fill="{t['hi']}"/>
<ellipse cx="310" cy="344" rx="50" ry="13" fill="{t['deep']}" opacity=".35"/>
<g fill="{t['deep']}" opacity=".3">
  <circle cx="288" cy="420" r="4"/><circle cx="310" cy="420" r="4"/><circle cx="332" cy="420" r="4"/>
  <circle cx="288" cy="448" r="4"/><circle cx="310" cy="448" r="4"/><circle cx="332" cy="448" r="4"/>
  <circle cx="288" cy="476" r="4"/><circle cx="310" cy="476" r="4"/><circle cx="332" cy="476" r="4"/>
</g>
<path d="M310 550 C330 590 370 600 420 606" stroke="#3a4a47" stroke-width="7" fill="none" stroke-linecap="round" opacity=".5"/>
<rect x="248" y="510" width="124" height="18" rx="9" fill="{t['deep']}" opacity=".28"/>
""", "Asiajoly pump", p)


DETAIL = {
    "fountain": ["190 300 250 250", "120 430 300 300"],
    "fountain-ceramic": ["180 310 260 260", "120 440 300 300"],
    "feeder": ["170 300 280 240", "150 420 320 260"],
    "bowl": ["170 320 280 240", "130 400 340 240"],
    "mat": ["140 380 340 220", "90 360 440 220"],
    "snuffle": ["150 350 320 230", "100 340 420 240"],
    "ball": ["200 360 220 220", "170 400 280 240"],
    "filter": ["220 320 180 220", "200 380 220 200"],
    "pump": ["230 320 160 220", "220 380 180 200"],
}

VB = {
    "fountain": "70 268 480 480",
    "fountain-ceramic": "80 290 460 440",
    "feeder": "138 288 344 404",
    "bowl": "128 306 364 336",
    "mat": "72 348 476 264",
    "snuffle": "88 330 444 256",
    "ball": "152 320 316 316",
    "filter": "188 308 244 304",
    "pump": "218 308 204 322",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for pid, form, base, opt in ART:
        if form == "fountain":
            s = fountain(base, small=(opt == "small"))
        elif form == "fountain-ceramic":
            s = fountain_ceramic(base)
        elif form == "feeder":
            s = feeder(base, small=(opt == "small"))
        elif form == "bowl":
            s = bowl(base)
        elif form == "mat":
            s = mat(base)
        elif form == "snuffle":
            s = snuffle(base)
        elif form == "ball":
            s = ball(base)
        elif form == "filter":
            s = filter(base)
        elif form == "pump":
            s = pump(base)
        else:
            raise SystemExit("unknown form " + form)
        s = s.replace('viewBox="0 0 620 760" width="620" height="760"',
                      'viewBox="%s" width="620" height="760"' % VB[form])
        (OUT / f"{pid}.svg").write_text(s, encoding="utf-8")
        d1, d2 = DETAIL[form]
        (OUT / f"{pid}-a.svg").write_text(
            s.replace('viewBox="%s"' % VB[form], 'viewBox="%s"' % d1), encoding="utf-8")
        (OUT / f"{pid}-b.svg").write_text(
            s.replace('viewBox="%s"' % VB[form], 'viewBox="%s"' % d2), encoding="utf-8")
        made.append(pid)

    # pro variants reuse the base drawing with a darker finish
    _pro = fountain("#3b4644").replace('viewBox="0 0 620 760"', 'viewBox="%s"' % VB["fountain"])
    (OUT / "spring-01-pro.svg").write_text(_pro, encoding="utf-8")
    made.append("spring-01-pro")
    _pfeed = feeder("#3b4644", camera=True).replace('viewBox="0 0 620 760"', 'viewBox="%s"' % VB["feeder"])
    (OUT / "feast-01-pro.svg").write_text(_pfeed, encoding="utf-8")
    made.append("feast-01-pro")
    # hero: the flagship in the brightest finish
    _hero = fountain("#c9d0d3").replace('viewBox="0 0 620 760"', 'viewBox="%s"' % VB["fountain"])
    (OUT / "hero.svg").write_text(_hero, encoding="utf-8")
    print("wrote", len(made), "product svgs")


if __name__ == "__main__":
    main()
