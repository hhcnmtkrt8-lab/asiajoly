#!/usr/bin/env python3
"""Render 1200x630 social cards for every shareable page.

Uses headless Chrome to screenshot a small HTML template — no image libraries, no
fonts to install, and the cards inherit the site's own type and colours.

Run: python3 build_og.py   (after build_art.py, before/after build_site.py)
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / ".build"
OUT = HERE / "assets" / "og"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BG = "#fdfbf7"
INK = "#14201f"
TEAL = "#12736b"
CORAL = "#e8734a"
MINT = "#e7f0ea"


def load(name, lang="en"):
    return json.loads((BUILD / f"{name}.json").read_text(encoding="utf-8"))[lang]


SITE = load("site")
PRODUCTS = load("products")
JOURNAL = load("journal")

CARDS = []  # (slug, kicker, title, sub, image, tint)

CARDS.append(("home", "PET OBJECTS · US & EU",
              "Calm, clean objects for cats and dogs",
              "Fountains, feeders, bowls and toys designed like good kitchen tools.",
              "assets/products/hero.svg", MINT))
CARDS.append(("shop", "SHOP",
              "Everything, in one place",
              "Four lines and the parts that keep them running.",
              "assets/products/spring-01.svg", "#f2ead9"))

for p in PRODUCTS:
    CARDS.append((f"p-{p['id']}", f"{p['line'].upper()} · {p['category'].upper()}",
                  f"{p['name']} — {p['tagline']}" if len(p["tagline"]) < 46 else p["name"],
                  p["tagline"] if len(p["tagline"]) < 46 else p["desc"][:110],
                  f"assets/products/{p['id']}.svg",
                  MINT if p["category"] == "Fountains" else "#f2ead9"))

CARDS.append(("about", "ABOUT", SITE["about"]["title"], SITE["about"]["sub"],
              "assets/products/hero.svg", "#e6eef2"))
CARDS.append(("technology", "TECHNOLOGY", SITE["technology"]["title"],
              SITE["technology"]["sub"], "assets/products/spring-01.svg", MINT))
CARDS.append(("journal", "JOURNAL", JOURNAL["index"]["title"], JOURNAL["index"]["sub"],
              "assets/products/still-bowl.svg", "#f2ead9"))
for i, a in enumerate(JOURNAL["articles"]):
    CARDS.append((f"journal-{i+1}", f"JOURNAL · {a['tag'].upper()}", a["title"], a["excerpt"],
                  "assets/products/filter-3.svg", MINT if i == 0 else "#f2ead9"))
CARDS.append(("faq", "FAQ", SITE["faq"]["title"], SITE["faq"]["sub"],
              "assets/products/still-mat.svg", "#e6eef2"))
CARDS.append(("contact", "CONTACT", SITE["contact"]["title"], SITE["contact"]["sub"],
              "assets/products/pump.svg", "#f2ead9"))
CARDS.append(("wholesale", "WHOLESALE", "Stock Asiajoly", SITE["footer"]["tagline"],
              "assets/products/feast-01.svg", MINT))
for slug in ("shipping", "returns", "warranty", "privacy", "terms"):
    d = load("legal")[slug]
    CARDS.append((slug, "POLICY", d["title"], d["intro"][:120],
                  "assets/products/filter-3.svg", "#f2ead9"))

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
  *{{box-sizing:border-box;margin:0}}
  body{{width:1200px;height:630px;background:{bg};font-family:"Helvetica Neue",Helvetica,Arial,
        "PingFang SC",sans-serif;color:{ink};overflow:hidden;position:relative}}
  .grid{{position:absolute;inset:0;display:grid;grid-template-columns:1.12fr .88fr}}
  .left{{padding:64px 20px 64px 72px;display:flex;flex-direction:column;justify-content:space-between}}
  .brand{{font-size:20px;letter-spacing:.22em;font-weight:600;text-transform:uppercase}}
  .brand em{{font-style:normal;color:{coral}}}
  .kicker{{font-family:ui-monospace,Menlo,monospace;font-size:13px;letter-spacing:.2em;
          color:{teal};text-transform:uppercase;margin-bottom:18px}}
  h1{{font-size:{hsize};line-height:1.02;letter-spacing:-.035em;font-weight:500;max-width:14ch}}
  p{{margin-top:20px;font-size:19px;line-height:1.5;color:#4a5a55;max-width:30ch}}
  .foot{{display:flex;align-items:center;gap:12px;font-family:ui-monospace,Menlo,monospace;
        font-size:12px;letter-spacing:.16em;color:#6d7a75;text-transform:uppercase}}
  .dot{{width:7px;height:7px;border-radius:50%;background:{teal}}}
  .right{{position:relative;background:{tint};display:grid;place-items:center}}
  .right:before{{content:"";position:absolute;width:430px;height:430px;border-radius:50%;
                 background:#fff;opacity:.55}}
  .right img{{position:relative;width:74%;filter:drop-shadow(0 40px 50px rgba(20,32,31,.22))}}
</style></head><body>
<div class="grid">
  <div class="left">
    <div>
      <div class="brand">ASIA<em>JOLY</em></div>
      <div style="margin-top:44px"><div class="kicker">{kicker}</div>
      <h1>{title}</h1><p>{sub}</p></div>
    </div>
    <div class="foot"><span class="dot"></span><span>asiajoly.com</span></div>
  </div>
  <div class="right"><img src="{img}"></div>
</div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = BUILD / "og"
    tmp.mkdir(parents=True, exist_ok=True)
    if not pathlib.Path(CHROME).exists():
        sys.exit("Chrome not found; run this on the machine that rendered the site")

    made = 0
    for slug, kicker, title, sub, img, tint in CARDS:
        title = " ".join(str(title).split())
        sub = " ".join(str(sub).split())
        hsize = "62px" if len(title) < 44 else ("52px" if len(title) < 62 else "44px")
        html = TEMPLATE.format(bg=BG, ink=INK, teal=TEAL, coral=CORAL, tint=tint,
                               kicker=kicker.replace("{", ""), title=title, sub=sub[:150],
                               img=str(HERE / img), hsize=hsize)
        page = tmp / f"{slug}.html"
        page.write_text(html, encoding="utf-8")
        out = OUT / f"{slug}.png"
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,630",
                        "--virtual-time-budget=1200",
                        f"--screenshot={out}", f"file://{page}"],
                       capture_output=True, timeout=90)
        made += 1
    print(f"rendered {made} social cards into assets/og/")


if __name__ == "__main__":
    main()
